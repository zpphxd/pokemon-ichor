local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local function oath() return L.ichor() + S.OFF_OATH end
local function state() return emu:read8(oath() + S.OFF_OATH_STATE) end
local function menu()
  L.waitUntil(function()
    if L.taskRunning("Task_HandleMultichoiceInput") then return true end
    L.tap(K.A); L.wait(20)
    return false
  end, 4500, "the native Oath YES/NO menu")
  L.wait(20)
end
local function confirmation()
  L.tap(K.UP); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_HandleYesNoInput") end, 600, "the Oath confirmation")
  L.wait(20)
end

L.start(function()
  L.quickstart()
  L.expect(L.getFlag(S.FLAG_OATH_CHOICE_PENDING) and not L.getFlag(S.FLAG_GOT_STARTER),
           "only a genuinely new game begins eligible for the pre-partner Oath choice")
  L.runHeader("Oath_ChoiceHeader", { noSettle = true })
  menu(); L.shot("default_no")
  L.tap(K.A); L.settle()
  L.expect(state() == S.ICHOR_OATH_DECLINED and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING)
           and emu:read16(oath() + S.OFF_OATH_URN_BOXES) == 0,
           "the menu defaults to NO and declining leaves every jar ordinary")
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  L.expect(state() == S.ICHOR_OATH_DECLINED and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING),
           "declining survives real save/reset/CONTINUE")
  L.runHeader("Oath_ChoiceHeader")
  L.expect(state() == S.ICHOR_OATH_DECLINED, "reopening the prompt cannot reverse a declined choice")

  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_UNDECIDED)
  L.runHeader("Oath_ChoiceHeader")
  L.expect(state() == S.ICHOR_OATH_UNDECIDED and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING),
           "an old-save fixture without the new-game flag is not prompted or retroactively enrolled")
  L.setFlag(S.FLAG_OATH_CHOICE_PENDING)
  L.setFlag(S.FLAG_GOT_STARTER)
  L.runHeader("Oath_ChoiceHeader")
  L.expect(state() == S.ICHOR_OATH_UNDECIDED,
           "having a first partner blocks late enrollment even with stale eligibility")
  L.setFlag(S.FLAG_GOT_STARTER, false)

  for difficulty = 0, 2 do
    emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_UNDECIDED)
    L.setFlag(S.FLAG_OATH_CHOICE_PENDING)
    L.setFlag(S.FLAG_DIFFICULTY_CHOSEN)
    L.setVar(S.VAR_DIFFICULTY, difficulty)
    L.runHeader("Oath_ChoiceHeader", { noSettle = true })
    menu()
    if difficulty == 0 then
      confirmation(); L.shot("binding_confirmation")
      L.tap(K.DOWN); L.tap(K.A)
      menu()
      L.expect(state() == S.ICHOR_OATH_UNDECIDED and L.getFlag(S.FLAG_OATH_CHOICE_PENDING),
               "refusing the binding confirmation returns to the choice without enrolling")
    end
    confirmation(); L.tap(K.A); L.settle()
    L.shot("oath_sworn_" .. difficulty)
    L.expect(state() == S.ICHOR_OATH_ACTIVE and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING)
             and emu:read16(oath() + S.OFF_OATH_URN_BOXES) == 1 << (S.TOTAL_BOXES_COUNT - 1),
             "confirming the real opening prompt swears the Oath and reserves its Urn on mode " .. difficulty)
    L.expect(L.getVar(S.VAR_DIFFICULTY) == difficulty and L.getFlag(S.FLAG_DIFFICULTY_CHOSEN),
             "Oath selection leaves the independently chosen difficulty unchanged")
    L.runHeader("Oath_SaveHeader")
    emu:reset(); L.continueSave()
    L.expect(state() == S.ICHOR_OATH_ACTIVE and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING)
             and emu:read16(oath() + S.OFF_OATH_URN_BOXES) == 1 << (S.TOTAL_BOXES_COUNT - 1)
             and L.getVar(S.VAR_DIFFICULTY) == difficulty,
             "the sworn Oath, Urn and separate difficulty survive real save/reset/CONTINUE")
    L.runHeader("Oath_ChoiceHeader")
    L.expect(state() == S.ICHOR_OATH_ACTIVE, "reopening the prompt cannot change a sworn choice")
  end

  emu:write8(oath() + S.OFF_OATH_STATE, S.ICHOR_OATH_UNDECIDED)
  L.setFlag(S.FLAG_OATH_CHOICE_PENDING)
  L.setFlag(S.FLAG_SET_WATER_CLOCK, false)
  L.runHeader("Oath_ClockHeader", { noSettle = true })
  L.waitUntil(function()
    if L.taskRunning("Task_SetClock_HandleInput") then return true end
    L.tap(K.A); L.wait(20)
    return false
  end, 1500, "the native water-clock setting screen")
  L.wait(30); L.tap(K.A)
  L.waitUntil(function() return L.taskRunning("Task_SetClock_HandleConfirmInput") end, 300, "clock confirmation")
  L.tap(K.UP); L.tap(K.A)
  menu(); confirmation(); L.tap(K.A); L.settle()
  L.shot("water_clock_flow_complete")
  L.expect(L.getFlag(S.FLAG_SET_WATER_CLOCK) and state() == S.ICHOR_OATH_ACTIVE
           and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING) and L.getVar(S.VAR_DIFFICULTY) == 2,
           "the actual water-clock screen returns through the native opening script and completes Oath enrollment")
  L.runHeader("Oath_SaveHeader")
  emu:reset(); L.continueSave()
  L.expect(L.getFlag(S.FLAG_SET_WATER_CLOCK) and state() == S.ICHOR_OATH_ACTIVE
           and not L.getFlag(S.FLAG_OATH_CHOICE_PENDING),
           "the complete clock-to-Oath opening persists through real save/reset/CONTINUE")
end)
