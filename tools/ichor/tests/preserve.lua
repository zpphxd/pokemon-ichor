-- The Erymanthian Preserve, Ichor's Safari Zone (tools/ichor/maps/erymanthos.py; the engine
-- switches in include/config/ichor.h): enter through the keeper's lodge, hunt with barley
-- and Pan Balls, run out of steps, hear the bell and be walked back to the lodge.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local extra = dofile(L.OUT .. "preserve_syms.lua")
for k, v in pairs(extra.SCRIPTS) do S.SCRIPTS[k] = v end
for k, v in pairs(extra) do if k ~= "SCRIPTS" then S[k] = v end end
local expect = L.expect

local function balls() return emu:read8(S.gNumSafariBalls) end
local function steps() return emu:read16(S.gSafariZoneStepCounter) end
local function safari() return L.getFlag(S.FLAG_SYS_SAFARI_MODE) end
local function actionMenu()
  return L.inBattle() and emu:read32(S.gBattlerControllerFuncs) == (S.SafariChooseAction | 1)
end
-- press A through the battle's messages until the action menu is up (or the battle is over)
local function waitMenuOrEnd(what)
  for _ = 1, 400 do
    if actionMenu() or L.inOverworld() then return end
    L.wait(8)
    if not actionMenu() and not L.inOverworld() then L.tap(K.A) end
  end
  L.shot("stuck_" .. what:gsub("%W", "_"))
  L.fail("never reached " .. what)
end

L.start(function()
  expect(S.SafariChooseAction ~= nil, "the Safari controller's action menu is in the symbols")
  L.quickstart()
  L.runHeader("Preserve_SetupHeader")
  L.settle()
  expect(L.mapId() == S.MAP_ARKADIA, "the test starts on Arkadia's west road")
  L.shot("arkadia_west_road")

  -- the keeper's hut at the road's end, and in
  L.useWarp(S.MAP_LODGE)
  expect(L.mapId() == S.MAP_LODGE, "the hut on Arkadia's west road is the Preserve's lodge")
  L.shot("lodge")
  local money = L.money()
  L.talk(L.npc("ErymanthosPreserve_Lodge_EventScript_Keeper"), { answers = { "yes" },
         stop = function() return L.mapId() == S.MAP_OAKWOOD end })
  L.waitUntil(function() return L.mapId() == S.MAP_OAKWOOD and L.idle() end, 600, "the walk into the Oakwood")
  L.settle()
  expect(L.mapId() == S.MAP_OAKWOOD, "the keeper takes the fee and lets the player into the Oakwood")
  expect(L.money() == money - 500, string.format("the fee is ¥500 (paid %d)", money - L.money()))
  expect(safari(), "the hunt is on (FLAG_SYS_SAFARI_MODE)")
  expect(balls() == S.ICHOR_SAFARI_BALLS, string.format("%d Pan Balls handed over (%d)", S.ICHOR_SAFARI_BALLS, balls()))
  expect(steps() == S.ICHOR_SAFARI_STEPS, string.format("%d steps to hunt in (%d)", S.ICHOR_SAFARI_STEPS, steps()))
  local x, y = L.pos()
  expect(x == 19 and y == 30, string.format("the hunt starts at the gate (%d,%d)", x, y))
  L.shot("oakwood_gate")

  -- the long glade: walk the tall grass until something comes out
  L.go(19, 25)
  L.go(17, 22)
  local before = steps()
  expect(before < S.ICHOR_SAFARI_STEPS, string.format("walking spends steps (%d left)", before))

  -- one hunt: walk the grass until something comes out, then barley (the first time) and
  -- Pan Balls until it's caught or it bolts. Returns the balls thrown and the outcome.
  local function hunt(barley)
    local met = false
    for i = 1, 400 do
      L.step((i % 2 == 0) and K.LEFT or K.RIGHT)
      if L.inBattle() then met = true break end
    end
    expect(met, "a wild Pokémon in the Oakwood's tall grass")
    waitMenuOrEnd("the Preserve's action menu")
    if L.inOverworld() then return 0, emu:read8(S.gBattleOutcome) end
    expect(emu:read32(S.gBattleTypeFlags) & S.BATTLE_TYPE_SAFARI ~= 0, "it's a Safari battle")
    if barley then
      L.shot("hunt_menu")
      L.tap(K.RIGHT); L.wait(4); L.tap(K.A)
      waitMenuOrEnd("the barley")
      L.shot("after_barley")
    end
    local start = balls()
    for _ = 1, 3000 do
      if L.inOverworld() then break end
      if actionMenu() then
        L.tap(K.UP); L.tap(K.LEFT); L.tap(K.A)
        L.wait(30)
      elseif L.on("CB2_NamingScreen") then
        L.acceptName("nickname")
      elseif L.taskRunning("Task_HandleYesNoInput") then
        L.tap(K.B); L.wait(10)
      else
        L.tap(K.A); L.wait(6)
      end
    end
    L.settle()
    return start - balls(), emu:read8(S.gBattleOutcome)
  end

  local thrown, outcome, hunts = 0, nil, 0
  repeat
    hunts = hunts + 1
    local n
    n, outcome = hunt(hunts == 1)
    thrown = thrown + n
    L.log(string.format("PRESERVE hunt %d: %d Pan Balls, outcome %d, %d left", hunts, n, outcome, balls()))
    expect(outcome == S.B_OUTCOME_CAUGHT or outcome == S.B_OUTCOME_MON_FLED,
           string.format("hunt %d ends caught or fled (outcome %d)", hunts, outcome))
  until (thrown > 0 and outcome == S.B_OUTCOME_CAUGHT) or hunts == 6
  expect(thrown > 0, string.format("Pan Balls were thrown (%d in %d hunts)", thrown, hunts))
  expect(balls() < S.ICHOR_SAFARI_BALLS, string.format("the Pan Balls run down (%d left)", balls()))
  expect(L.mapId() == S.MAP_OAKWOOD and safari(), "back in the Oakwood, still hunting")
  L.shot("after_the_hunt")

  -- the last steps: the keeper's bell, and the walk back to the lodge
  L.go(19, 25)
  emu:write16(S.gSafariZoneStepCounter, 3)
  L.step(K.DOWN); L.step(K.DOWN)
  L.step(K.DOWN)
  L.settle({ stop = function() return L.mapId() == S.MAP_LODGE end })
  L.waitUntil(function() return L.mapId() == S.MAP_LODGE end, 1200, "the bell's walk back to the lodge")
  L.shot("rung_out")
  L.settle()
  expect(L.mapId() == S.MAP_LODGE, "out of steps, the player is walked back to the lodge")
  expect(not safari(), "the hunt is over (FLAG_SYS_SAFARI_MODE clear)")
  expect(L.getVar(S.VAR_SAFARI_ZONE_STATE) == 0, "the keeper's welcome back has played")
  x, y = L.pos()
  expect(x == 5 and y == 5, string.format("the hunt ends in front of the keeper (%d,%d)", x, y))
  L.shot("lodge_after")
  L.useWarp(S.MAP_ARKADIA)
  expect(L.mapId() == S.MAP_ARKADIA, "the lodge's door leads back out to Arkadia")
end)
