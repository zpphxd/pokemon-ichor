-- Sherds are fixture inputs; restoration, clock transitions and battles are real.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local SHELF = "ElaiaVillage_Akademia_EventScript_Scrolls"
local ALTAR = "KallisteRoute1_KronionHill_EventScript_Altar"
local PERSEPHONE = "EleusaVillage_EventScript_AmphoraPersenyx"
local ARACHNE = "HecatesHollow_EventScript_Raknit"
S.SCRIPTS[ARACHNE] = S.HecatesHollow_EventScript_Raknit

local function visit(name) L.runHeader("AmphoraLeads_" .. name .. "Header") end
local function hold(tod)
  L.setVar(S.VAR_0x8004, tod)
  visit("Hold")
end
local function clock(hour, minute, second, held)
  L.setVar(S.VAR_0x8004, hour)
  L.setVar(S.VAR_0x8005, minute or 0)
  L.setVar(S.VAR_0x8006, second or 0)
  L.runHeader("AmphoraLeads_" .. (held and "HeldClock" or "Clock") .. "Header", { noSettle = held })
end
local function present() return L.objectAt(S.LOCALID_PERSENYX) ~= nil end
local function saveAndContinue()
  visit("Save")
  emu:reset()
  L.continueSave()
end

local function begin(target, lead)
  L.talk(target, { answers = { "yes" }, stop = L.inBattle })
  L.waitUntil(function()
    if emu:read32(S.gBattlerControllerFuncs) == (S.HandleInputChooseAction | 1) then return true end
    L.tap(K.A); L.wait(4)
    return false
  end, 1200, lead.name .. "'s battle action menu")
  local enemy = S.gBattleMons + S.BATTLE_MON_SIZE
  L.expect(emu:read16(enemy + S.OFF_BATTLE_SPECIES) == lead.species
           and emu:read8(enemy + S.OFF_BATTLE_LEVEL) == lead.level,
           lead.name .. " has its designed species and exact level")
  if lead.ability then
    L.expect(emu:read16(enemy + S.OFF_BATTLE_ABILITY) == lead.ability,
             lead.name .. " has its actual designed hidden ability")
  end
  if lead.item then
    L.expect(emu:read16(enemy + S.OFF_BATTLE_ITEM) == lead.item,
             lead.name .. " really holds its designed item")
  end
  L.shot(lead.name .. "_battle")
end

local function capture()
  local balls = L.itemCount(S.ITEM_MASTER_BALL)
  local count = emu:read8(S.gPartiesCount)
  L.tap(K.UP); L.tap(K.RIGHT); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_BagMenu_HandleInput") end, 1200, "the real battle Bag")
  L.wait(30)
  for _ = 1, S.POCKETS_COUNT do
    if emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS then break end
    L.tap(K.RIGHT); L.wait(50)
  end
  L.expect(emu:read8(S.gBagPosition + S.OFF_BAG_POSITION_POCKET) == S.POCKET_POKE_BALLS,
           "the battle Bag reaches the real ball pocket")
  L.tap(K.UP); L.tap(K.UP); L.tap(K.A); L.wait(20); L.tap(K.A)
  L.waitUntil(function()
    if L.inOverworld() then return true end
    if L.on("CB2_NamingScreen") then L.acceptName("captured_lead") else L.tap(K.A); L.wait(4) end
    return false
  end, 12000, "capture and return to the field")
  L.settle()
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_CAUGHT
           and emu:read8(S.gPartiesCount) == count + 1
           and L.itemCount(S.ITEM_MASTER_BALL) == balls - 1,
           "a real capture adds a Pokemon and consumes exactly one ball (outcome "
           .. emu:read8(S.gBattleOutcome) .. ", party " .. count .. "->" .. emu:read8(S.gPartiesCount)
           .. ", balls " .. balls .. "->" .. L.itemCount(S.ITEM_MASTER_BALL) .. ")")
end

local function encounter(lead)
  hold(lead.tod)
  visit(lead.map)
  L.expect(L.partyLevel(0) == 100, "the saved battle-strength assist is intact")
  L.setFlag(S.FLAG_NO_RUNNING, false)
  local function target() return lead.sign and L.sign(lead.script) or L.npc(lead.script) end
  if not lead.sign then L.expect(target().present, lead.name .. " appears after genuine shelf restoration") end
  if lead.sign or lead.name == "Persenyx" then
    local before = #L.battles
    L.talk(target(), { answers = { "no" } })
    L.expect(#L.battles == before and not L.getFlag(lead.flag), "declining " .. lead.name .. " does not consume it")
  end
  local state = L.OUT .. lead.name .. "_pending.ss"
  L.expect(emu:saveStateFile(state, 31), "save the pending " .. lead.name .. " branch")
  local function restore()
    L.expect(emu:loadStateFile(state, 31), "restore the pending " .. lead.name .. " branch")
    L.wait(30)
  end

  begin(target(), lead)
  L.battle()
  L.settle()
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_RAN and not L.getFlag(lead.flag),
           "escaping " .. lead.name .. " preserves its one-time encounter")
  visit(lead.map)
  if not lead.sign then L.expect(target().present, "escaped " .. lead.name .. " survives real map reentry") end

  restore()
  visit("Weak")
  L.battleMode = "lose"
  L.setFlag(S.FLAG_NO_RUNNING, true)
  begin(target(), lead)
  L.battle()
  L.settle()
  L.battleMode = nil
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_LOST and not L.getFlag(lead.flag),
           "losing to " .. lead.name .. " does not claim it")
  visit(lead.map)
  if not lead.sign then L.expect(target().present, "lost " .. lead.name .. " remains available after whiteout") end

  restore()
  L.setFlag(S.FLAG_NO_RUNNING, true)
  begin(target(), lead)
  L.battle()
  L.settle()
  L.expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_WON and L.getFlag(lead.flag),
           "defeating " .. lead.name .. " claims only its encounter")

  restore()
  begin(target(), lead)
  capture()
  L.expect(L.getFlag(lead.flag), "capturing " .. lead.name .. " sets its completion flag")
  if not lead.sign then L.expect(not target().present, "claimed " .. lead.name .. " disappears without needing reentry") end
  saveAndContinue()
  L.expect(L.getFlag(lead.flag), "the captured " .. lead.name .. " remains claimed after CONTINUE")
  visit(lead.map)
  if lead.sign then
    local before = #L.battles
    L.talk(target())
    L.expect(#L.battles == before, "the claimed altar cannot grant another Cairnolith")
  else
    L.expect(not target().present, "claimed " .. lead.name .. " cannot respawn on reentry")
  end
end

L.start(function()
  L.expect(S.Task_BagMenu_HandleInput ~= nil and S.gPartiesCount ~= nil
           and S.gBattleMons ~= nil and S.SCRIPTS[ARACHNE] ~= nil,
           "all required native battle and Hollow symbols are resolved")
  L.quickstart()
  visit("Setup")
  for amphora = 0, 2 do
    for piece = 0, 3 do L.setFlag(S.FLAG_SHERDS + amphora * 4 + piece, true) end
  end
  hold(S.TIME_NIGHT)
  visit("Kronion")
  local before = #L.battles
  L.talk(L.sign(ALTAR))
  L.expect(#L.battles == before and not L.getFlag(S.FLAG_CAIRNOLITH),
           "four collected Kronos sherds alone do not unlock the altar")
  hold(S.TIME_EVENING)
  visit("Eleusa")
  L.expect(not present(), "four Persephone sherds without restoration do not reveal the dusk visitor")
  visit("Hollow")
  L.expect(not L.npc(ARACHNE).present, "four Arachne sherds without restoration do not reveal Raknit")
  visit("Akademia")
  for amphora = 0, 2 do
    L.talk(L.sign(SHELF), { answers = { amphora, "yes" } })
    L.expect(L.getFlag(S.FLAG_AMPHORAE + amphora), "the real shelf restores Act I amphora " .. amphora)
  end
  hold(S.TIME_DAY)
  visit("Kronion")
  before = #L.battles
  L.talk(L.sign(ALTAR))
  L.expect(#L.battles == before, "restored Kronos still waits for night")
  visit("Eleusa")
  L.expect(not present(), "restored Persephone still waits for dusk")
  visit("Spot")
  clock(S.EVENING_BEGIN - 1, 59, 59)
  L.waitUntil(function() return emu:read8(S.gLocalTime + S.OFF_TIME_HOURS) == S.EVENING_BEGIN end,
              9000, "the actual dusk clock boundary")
  L.wait(120)
  L.expect(not present() and not L.getFlag(S.FLAG_PERSENYX_HIDDEN),
           "the actual dusk arrival waits while the player occupies its tile")
  saveAndContinue()
  local x, y = L.pos()
  L.expect(not present() and x == 37 and y == 33,
           "CONTINUE does not materialize the pending visitor on top of the player")
  L.go(38, 33)
  L.waitUntil(present, 600, "the dusk visitor after vacating its tile")
  L.shot("persenyx_dusk_arrival")
  clock(S.EVENING_END - 1, 59, 59)
  L.waitUntil(function() return emu:read8(S.gLocalTime + S.OFF_TIME_HOURS) == S.EVENING_END end,
              9000, "the actual end of dusk")
  L.waitUntil(function() return not present() end, 600, "the visitor's live dusk expiry")
  L.expect(L.getFlag(S.FLAG_PERSENYX_HIDDEN) and not L.getFlag(S.FLAG_PERSENYX),
           "live dusk expiry hides but does not claim the visitor")
  clock(S.EVENING_BEGIN, 0, 0, true)
  L.wait(60)
  L.expect(not present(), "an active script defers the dusk arrival")
  L.setFlag(S.FLAG_FROZEN, true)
  L.settle()
  L.expect(not present(), "the Frozen Hour preserves the deferred arrival")
  L.setFlag(S.FLAG_FROZEN, false)
  L.waitUntil(present, 600, "the visitor after script control and time return")
  L.expect(present(), "the deferred dusk arrival resumes safely")

  visit("Strong")
  L.assistLevel100()
  encounter({ name = "Cairnolith", map = "Kronion", script = ALTAR, sign = true, tod = S.TIME_NIGHT,
              species = S.SPECIES_CAIRNOLITH, level = 20, ability = S.ABILITY_SAND_FORCE,
              item = S.ITEM_HARD_STONE, flag = S.FLAG_CAIRNOLITH })
  encounter({ name = "Raknit", map = "Hollow", script = ARACHNE, tod = S.TIME_DAY,
              species = S.SPECIES_RAKNIT, level = 20, ability = S.ABILITY_DEFIANT, flag = S.FLAG_RAKNIT })
  encounter({ name = "Persenyx", map = "Eleusa", script = PERSEPHONE, tod = S.TIME_EVENING,
              species = S.SPECIES_PERSENYX, level = 22, flag = S.FLAG_PERSENYX })
  L.expect(L.getFlag(S.FLAG_CAIRNOLITH) and L.getFlag(S.FLAG_RAKNIT) and L.getFlag(S.FLAG_PERSENYX),
           "all three actual captures retain independent completion")
end)
