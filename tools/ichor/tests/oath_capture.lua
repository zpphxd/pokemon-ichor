local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local function oath() return L.ichor() + S.OFF_OATH end
local function receipts() return L.snapshot(oath() + S.OFF_OATH_ENCOUNTERS, 32) end
local function urnStorage()
  return emu:read32(S.gPokemonStoragePtr) + S.OFF_STORAGE_BOXES + (S.TOTAL_BOXES_COUNT - 1) * S.BOX_BYTES
end

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

local function faintLead()
  local falls = emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT)
  L.runHeader("Oath_FaintHeader", { noSettle = true })
  L.waitUntil(function()
    if emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) > falls then return true end
    if emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) then
      L.tap(K.UP); L.tap(K.LEFT); L.tap(K.A)
    else
      L.tap(K.A)
    end
    L.wait(4)
    return false
  end, 12000, "a real opponent fainting the weak lead")
  L.expect(emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) == falls + 1 and L.partyHp(0) == 0,
           "actual battle fainting records the player partner exactly once")
  local fallen = L.snapshot(S.gParties, S.BOX_MON_BYTES)
  L.waitUntil(function()
    if L.taskRunning("Task_HandleChooseMonInput") then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 2000, "the native replacement party menu")
  L.wait(60)
  L.tap(K.RIGHT); L.tap(K.A); L.wait(30); L.tap(K.A)
  L.waitUntil(function()
    if L.inBattle() then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 2000, "the living partner to enter battle")
  L.battle()
  L.waitUntil(function() return emu:read8(S.sOathAftermathNotice) & 0x80 ~= 0 end,
              1200, "the post-battle Urn notice")
  L.wait(120)
  return falls, fallen
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

  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_ACTIVE)
  local falls, fallenBox = faintLead()
  L.shot("urn_automatic_transfer")
  L.expect(emu:read8(S.sLockFieldControls) ~= 0
           and emu:read8(S.sOathAftermathNotice) & 0x7F == S.ICHOR_URN_STORED,
           "the native aftermath notice keeps controls locked until acknowledged")
  L.expect(emu:read8(S.gPartiesCount) == 1 and L.partyHp(0) > 0
           and L.snapshot(urnStorage(), S.BOX_MON_BYTES) == fallenBox,
           "native battle teardown transfers the whole fallen partner and compacts its living replacement")
  L.settle()
  L.runHeader("Oath_HealHeader")
  L.expect(L.partyHp(0) > 0 and L.snapshot(urnStorage(), S.BOX_MON_BYTES) == fallenBox,
           "native party healing cannot modify the fallen partner in the Urn")
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  L.runHeader("Oath_HealHeader")
  L.expect(emu:read8(S.gPartiesCount) == 1
           and L.snapshot(urnStorage(), S.BOX_MON_BYTES) == fallenBox
           and emu:read16(oath() + S.OFF_OATH_FALLEN_COUNT) == falls + 1,
           "automatic transfer, fallen identity and the compacted party survive save/reset/CONTINUE")
  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_RELEASED)
  L.runHeader("Oath_HealHeader")
  L.expect(L.snapshot(urnStorage(), S.BOX_MON_BYTES) == fallenBox,
           "ending the Oath does not bring back already fallen partners")

  L.runHeader("Oath_UrnHeader")
  local storage = emu:read32(S.gPokemonStoragePtr)
  local urn = S.TOTAL_BOXES_COUNT - 1
  local urnAddr = storage + S.OFF_STORAGE_BOXES + urn * S.BOX_BYTES
  -- The Urn is native battle output; only the ordinary PC partners are seeded.
  for i = 0, S.BOX_MON_BYTES - 1 do
    for slot = 0, 1 do
      emu:write8(storage + S.OFF_STORAGE_BOXES + slot * S.BOX_MON_BYTES + i,
                 emu:read8(S.gParties + i))
    end
  end
  local before = L.snapshot(urnAddr, S.BOX_BYTES)
  local urnName = storage + S.OFF_STORAGE_NAMES + urn * S.BOX_NAME_BYTES
  local name = L.snapshot(urnName, S.BOX_NAME_BYTES)
  emu:write8(storage, urn)
  L.runHeader("Oath_PcHeader", { noSettle = true })
  L.waitUntil(function() return L.taskRunning("Task_PCMainMenu") end, 900, "the native Pithos menu")
  L.wait(90); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_PokeStorageMain") end, 1200, "Move partners")
  L.wait(120)
  L.shot("urn_view")

  local function menu()
    L.tap(K.A)
    L.waitUntil(function() return L.taskRunning("Task_OnSelectedMon") end, 300, "the Urn action menu")
    L.wait(60)
  end
  local function main()
    L.waitUntil(function() return L.taskRunning("Task_PokeStorageMain") end, 900, "the storage cursor")
    L.wait(90)
  end
  menu(); L.shot("urn_summary_only")
  L.tap(K.DOWN); L.tap(K.A); main()
  L.expect(L.snapshot(urnAddr, S.BOX_BYTES) == before and emu:read8(S.sIsMonBeingMoved) == 0,
           "the Urn action menu offers Cancel instead of any withdraw, release or move action")
  menu(); L.tap(K.A); L.wait(150)
  L.expect(not L.taskRunning("Task_PokeStorageMain") and emu:read32(S.sMonSummaryScreen) ~= 0,
           "fallen partners remain viewable in the real summary screen")
  L.shot("urn_summary")
  L.tap(K.RIGHT); L.wait(45); L.tap(K.RIGHT); L.wait(45)
  L.tap(K.A); L.wait(60); L.tap(K.A); L.wait(60); L.tap(K.DOWN); L.tap(K.A); L.wait(60)
  L.expect(L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "the summary move-order shortcut cannot mutate a fallen partner")
  L.shot("urn_moves")
  L.tap(K.B); L.wait(45); L.tap(K.LEFT); L.wait(45); L.tap(K.LEFT); L.wait(45)
  L.tap(K.A); L.wait(60)
  L.expect(not L.on("CB2_PssChangePokemonNickname")
           and L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "the fallen summary cannot enter the nickname editor")
  main()
  L.tap(K.SELECT)
  L.expect(emu:read8(S.sAutoActionOn) ~= 0, "the storage shortcut cursor is enabled")
  menu(); L.tap(K.DOWN); L.tap(K.A); main()
  L.expect(emu:read8(S.sIsMonBeingMoved) == 0 and L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "shortcut and group-selection mode cannot lift an Urn partner")
  L.tap(K.SELECT)
  L.tap(K.START); L.wait(60); L.tap(K.A); L.wait(60)
  L.shot("urn_box_options")
  L.tap(K.DOWN); L.tap(K.A); main()
  L.expect(L.snapshot(urnName, S.BOX_NAME_BYTES) == name,
           "Urn box options preserve its reserved name")
  L.tap(K.DOWN); L.wait(45)
  L.tap(K.RIGHT); L.wait(45); L.tap(K.A); L.wait(60)
  L.shot("urn_empty_slot_refusal")
  L.expect(L.snapshot(urnAddr, S.BOX_BYTES) == before and emu:read8(S.sIsMonBeingMoved) == 0,
           "an empty Urn slot refuses ordinary storage actions")
  L.tap(K.B); main()

  local function changeBox(key, expected)
    L.tap(K.START); L.wait(30); L.tap(key); L.wait(120)
    L.expect(emu:read8(storage) == expected, "the native cursor scrolls to jar " .. (expected + 1))
    L.tap(K.DOWN); L.wait(30)
    L.tap(K.LEFT); L.wait(20); L.tap(K.LEFT); L.wait(30)
  end
  changeBox(K.RIGHT, 0)
  menu(); L.tap(K.A); main()
  L.expect(emu:read8(S.sIsMonBeingMoved) ~= 0, "an ordinary jar still permits moving a living partner")
  changeBox(K.LEFT, urn)
  L.tap(K.RIGHT); L.wait(30)
  L.tap(K.A); L.wait(60); L.shot("urn_deposit_refusal")
  L.expect(emu:read8(S.sIsMonBeingMoved) ~= 0 and L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "A-button placement refuses an empty Urn slot without losing the held partner")
  L.tap(K.B); main()
  L.tap(K.B); L.wait(60)
  L.expect(emu:read8(S.sIsMonBeingMoved) ~= 0 and L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "B-button quick placement cannot bypass the sealed Urn")
  L.tap(K.A); main()
  changeBox(K.RIGHT, 0)
  menu(); L.tap(K.A); main()
  L.expect(emu:read8(S.sIsMonBeingMoved) == 0, "a refused placement can safely return its partner to ordinary storage")

  local ordinary = storage + S.OFF_STORAGE_BOXES
  local ordinaryBefore = L.snapshot(ordinary, S.BOX_MON_BYTES * 2)
  L.tap(K.SELECT)
  emu:addKey(K.A); L.wait(60); L.tap(K.RIGHT); L.wait(45); emu:clearKey(K.A)
  L.wait(120)
  L.expect(emu:read8(S.sIsMonBeingMoved) ~= 0 and L.snapshot(ordinary, S.BOX_MON_BYTES * 2) ~= ordinaryBefore,
           "ordinary storage still permits lifting a real multi-partner selection")
  L.tap(K.LEFT); L.wait(120)
  L.expect(emu:read8(storage) == urn, "a lifted group can scroll to the Urn")
  L.tap(K.A); L.wait(60); L.shot("urn_group_refusal")
  L.expect(emu:read8(S.sIsMonBeingMoved) ~= 0 and L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "a group cannot be placed in the Urn and remains safely held")
  L.tap(K.B); main()
  for _ = 1, 6 do
    if emu:read8(storage) == 0 then break end
    L.tap(K.RIGHT); L.wait(90)
  end
  for _ = 1, 4 do L.tap(K.LEFT); L.wait(30) end
  L.tap(K.A); L.wait(120)
  L.expect(emu:read8(storage) == 0 and emu:read8(S.sIsMonBeingMoved) == 0
           and L.snapshot(ordinary, S.BOX_MON_BYTES * 2) == ordinaryBefore,
           "a refused group can be returned with both ordinary partners intact")
  L.expect(L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "returning the group leaves every byte of the Urn unchanged")
  L.tap(K.SELECT)

  changeBox(K.LEFT, urn)
  L.tap(K.B); L.wait(60); L.tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_PCMainMenu") end, 1200, "the Pithos mode menu")
  L.wait(90)
  L.tap(K.DOWN); L.tap(K.DOWN); L.tap(K.DOWN); L.tap(K.A); main()
  storage = emu:read32(S.gPokemonStoragePtr)
  urnAddr = storage + S.OFF_STORAGE_BOXES + urn * S.BOX_BYTES
  L.tap(K.A); L.wait(60); L.shot("urn_item_refusal")
  L.expect(L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "Move items cannot take the fallen partner's held item or give it another")
  L.tap(K.B); main()
  L.tap(K.B); L.wait(60); L.tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_PCMainMenu") end, 1200, "the mode menu after Move items")
  L.wait(90)
  for i = 0, S.PARTY_MON_BYTES - 1 do
    emu:write8(S.gParties + S.PARTY_MON_BYTES + i, emu:read8(S.gParties + i))
  end
  emu:write8(S.gPartiesCount, 2)
  local party = L.snapshot(S.gParties, S.PARTY_MON_BYTES * 2)
  L.tap(K.UP); L.tap(K.UP); L.tap(K.A); main()
  menu(); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_DepositMenu") end, 600, "the party-deposit jar chooser")
  L.wait(90); L.tap(K.LEFT); L.wait(45); L.tap(K.A); L.wait(90)
  storage = emu:read32(S.gPokemonStoragePtr)
  urnAddr = storage + S.OFF_STORAGE_BOXES + urn * S.BOX_BYTES
  L.shot("urn_party_deposit_refusal")
  L.expect(emu:read8(S.gPartiesCount) == 2 and L.snapshot(S.gParties, S.PARTY_MON_BYTES * 2) == party
           and L.snapshot(urnAddr, S.BOX_BYTES) == before,
           "the party-deposit chooser refuses a reserved jar before changing either partner")
  L.tap(K.B); L.wait(60); L.tap(K.B); main()
  L.tap(K.B); L.wait(60); L.tap(K.B)
  L.waitUntil(function() return L.taskRunning("Task_PCMainMenu") end, 1200, "the mode menu after deposit refusal")
  L.wait(90); L.tap(K.B); L.settle()
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  storage = emu:read32(S.gPokemonStoragePtr)
  urnAddr = storage + S.OFF_STORAGE_BOXES + urn * S.BOX_BYTES
  L.expect(L.snapshot(urnAddr, S.BOX_BYTES) == before
           and emu:read8(oath() + S.OFF_OATH_STATE) == S.ICHOR_OATH_RELEASED
           and emu:read16(oath() + S.OFF_OATH_URN_BOXES) & (1 << urn) ~= 0,
           "the unchanged Urn and its reservation survive real save/reset/CONTINUE after release")

  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_ACTIVE)
  for i = 0, S.BOX_MON_BYTES - 1 do
    for box = 0, urn - 1 do
      emu:write8(storage + S.OFF_STORAGE_BOXES + box * S.BOX_BYTES + i, emu:read8(S.gParties + i))
    end
    for slot = 1, S.IN_BOX_COUNT - 1 do
      emu:write8(urnAddr + slot * S.BOX_MON_BYTES + i, emu:read8(urnAddr + i))
    end
  end
  local fullUrn = L.snapshot(urnAddr, S.BOX_BYTES)
  local _, retained = faintLead()
  L.shot("urn_capacity_refusal")
  L.expect(emu:read8(S.sOathAftermathNotice) & 0x7F == S.ICHOR_URN_FULL
           and emu:read8(S.sLockFieldControls) ~= 0,
           "a real full-capacity aftermath explicitly explains refusal before resuming the script")
  L.expect(emu:read8(S.gPartiesCount) == 2 and L.partyHp(0) == 0 and L.partyHp(1) > 0
           and L.snapshot(S.gParties, S.BOX_MON_BYTES) == retained
           and L.snapshot(urnStorage(), S.BOX_BYTES) == fullUrn,
           "full capacity preserves both the pending source and every existing Urn record")
  L.tap(K.A); L.wait(120); L.shot("urn_capacity_instructions")
  L.settle()
  L.runHeader("Oath_HealHeader")
  L.expect(L.partyHp(0) == 0, "a retained capacity-overflow partner still cannot be healed")
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  L.expect(L.partyHp(0) == 0 and emu:read8(S.gPartiesCount) == 2
           and L.snapshot(S.gParties, S.BOX_MON_BYTES) == retained
           and L.snapshot(urnStorage(), S.BOX_BYTES) == fullUrn,
           "capacity refusal retains the pending source and full Urn through save/reset/CONTINUE")
end)
