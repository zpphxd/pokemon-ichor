local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local function oath() return L.ichor() + S.OFF_OATH end
local function receipts() return L.snapshot(oath() + S.OFF_OATH_ENCOUNTERS, 32) end

local function begin()
  L.runHeader("Oath_BattleHeader", { noSettle = true })
  L.waitUntil(function()
    if emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 2000, "wild battle action menu")
end

local function openBall()
  L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "battle Bag")
  L.wait(30)
  for _ = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    L.tap(K.RIGHT); L.wait(50)
  end
  L.expect(emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS,
           "the real Bag opens its ball pocket")
  L.tap(K.UP); L.tap(K.UP); L.tap(K.A); L.wait(20); L.tap(K.A)
end

local function capture()
  local balls, count = L.itemCount(S.ITEM_MASTER_BALL), emu:read8(S.gPartiesCount)
  openBall()
  L.waitUntil(function()
    if L.inOverworld() then return true end
    if L.on("CB2_NamingScreen") then L.acceptName("caught") else L.tap(K.A); L.wait(4) end
    return false
  end, 12000, "real capture returning to the field")
  L.settle()
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_CAUGHT
           and emu:read8(S.gPartiesCount) == count + 1
           and L.itemCount(S.ITEM_MASTER_BALL) == balls - 1,
           "an allowed native capture adds one partner and consumes exactly one ball")
end

local function refuse()
  local balls, count, before = L.itemCount(S.ITEM_MASTER_BALL), emu:read8(S.gPartiesCount), receipts()
  local turn = emu:read8(S.gBattleResults + S.OFF_BATTLE_TURN)
  openBall()
  L.wait(180)
  L.expect(emu:read8(S.sOathCatchDenied) ~= 0, "the repeat-area battle has no catch permission")
  L.shot("repeat_area_refusal")
  L.expect(L.itemCount(S.ITEM_MASTER_BALL) == balls, "refusal preserves every ball")
  L.expect(emu:read8(S.gPartiesCount) == count and receipts() == before,
           "refusal preserves party and area receipts")
  L.expect(L.on("CB2_BagMenuRun"), "refusal stays in the Bag")
  L.expect(emu:read8(S.gBattleResults + S.OFF_BATTLE_TURN) == turn,
           "Bag refusal does not advance the battle turn")
  L.tap(K.A); L.wait(30); L.tap(K.B); L.wait(30); L.tap(K.B); L.wait(90)
  L.battle()
  L.settle()
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_RAN, "refused capture can still escape normally")
end

L.start(function()
  L.expect(S.sOathCatchDenied ~= nil, "the native capture-policy symbol is available")
  L.quickstart()
  L.runHeader("Oath_SetupHeader")
  -- The option remains gated: only this test enrolls a fixture save.
  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_ACTIVE)
  emu:write16(oath() + S.OFF_OATH_URN_BOXES, 1 << (S.TOTAL_BOXES_COUNT - 1))
  local empty = receipts()
  begin()
  L.expect(emu:read8(S.sOathCatchDenied) == 0 and receipts() ~= empty,
           "native battle entry grants and saves the first named-area chance")
  local first = receipts()
  capture()
  begin()
  L.expect(receipts() == first, "a second battle in the same named area adds no receipt")
  refuse()
  L.runHeader("Oath_RouteHeader")
  begin()
  L.expect(emu:read8(S.sOathCatchDenied) == 0 and receipts() ~= first,
           "another named area grants its own first chance")
  local second = receipts()
  L.battle(); L.settle()
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_RAN,
           "escaping spends that area's encounter chance without a capture")
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  L.expect(receipts() == second, "both area chances survive actual save/reset/CONTINUE")
  begin(); refuse()
  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_RELEASED)
  begin()
  L.expect(emu:read8(S.sOathCatchDenied) == 0 and receipts() == second,
           "release restores normal capture permission without deleting history")
  capture()
  L.shot("released_capture")
end)
