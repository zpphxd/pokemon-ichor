local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local trainers = dofile(L.OUT .. "trainers.lua").gTrainers

local function menu()
    local start = L.now()
    while not L.taskRunning("Task_HandleMultichoiceInput") do
        if L.now() - start > 3000 then L.fail("difficulty menu did not open") end
        L.tap(K.A)
        L.wait(25)
    end
    L.wait(15)
end

local function choose(difficulty)
    menu()
    L.shot("difficulty_choices")
    if difficulty == 0 then L.tap(K.UP) end
    if difficulty == 2 then L.tap(K.DOWN) end
    L.tap(K.A)
    L.settle()
end

local function parties()
    local bosses = {
        {S.TRAINER_IONE, {12, 13, 14}},
        {S.TRAINER_KERYKOS, {18, 19, 20}},
        {S.TRAINER_CHLOE_DAY, {24, 24, 25, 26}},
        {S.TRAINER_CHLOE_NIGHT, {24, 24, 25, 26}},
        {S.TRAINER_THESPIS, {30, 30, 31, 32}},
    }
    for _, boss in ipairs(bosses) do
        local normal = trainers + boss[1] * S.SIZE_TRAINER
            + S.TRAINER_COUNT * S.SIZE_TRAINER
        normal = emu:read32(normal + S.OFF_TRAINER_PARTY)
        for difficulty = 0, 2 do
            local trainer = trainers + (difficulty * S.TRAINER_COUNT + boss[1]) * S.SIZE_TRAINER
            local party = emu:read32(trainer + S.OFF_TRAINER_PARTY)
            L.expect(party >= 0x08000000 and party < 0x0A000000, "boss has a real party on difficulty " .. difficulty)
            for slot, level in ipairs(boss[2]) do
                local mon = party + (slot - 1) * S.SIZE_TRAINER_MON
                local hero = normal + (slot - 1) * S.SIZE_TRAINER_MON
                L.expect(emu:read8(mon + S.OFF_TRAINER_MON_LEVEL) == level - (difficulty == 0 and 3 or 0),
                         "boss level matches BALANCE for difficulty " .. difficulty .. " slot " .. slot)
                L.expect(emu:read16(mon + S.OFF_TRAINER_MON_SPECIES) == emu:read16(hero + S.OFF_TRAINER_MON_SPECIES),
                         "boss retains the Hero species")
                if difficulty == 2 then
                    local evs = emu:read32(mon + S.OFF_TRAINER_MON_EVS)
                    local total = 0
                    for stat = 0, 5 do total = total + emu:read8(evs + stat) end
                    L.expect(total == 508, "Spartan boss has a complete legal EV spread")
                end
            end
        end
    end
end

L.start(function()
    L.quickstart()
    parties()
    for difficulty = 0, 2 do
        L.setFlag(S.FLAG_DIFFICULTY_CHOSEN, false)
        L.runHeader("DifficultyMenuHeader", {noSettle = true})
        if difficulty == 2 then
            menu()
            L.tap(K.A)
            L.waitUntil(function() return L.taskRunning("Task_HandleYesNoInput") end, 600, "confirmation")
            L.wait(15)
            L.tap(K.DOWN)
            L.tap(K.A)
            menu()
            L.expect(not L.getFlag(S.FLAG_DIFFICULTY_CHOSEN), "declining confirmation does not lock the save")
        end
        choose(difficulty)
        L.expect(L.getFlag(S.FLAG_DIFFICULTY_CHOSEN), "confirmed difficulty is saved")
        L.expect(L.getVar(S.VAR_DIFFICULTY) == difficulty, "actual menu selected difficulty " .. difficulty)
        L.expect(L.getVar(S.VAR_0x8000) == difficulty, "script bank-var access matches the confirmed menu")
        L.expect(L.getVar(S.VAR_0x8001) == ({150, 120, 100})[difficulty + 1], "native step-glass limit matches difficulty")
        L.runHeader("DifficultyMenuHeader")
        L.expect(L.getVar(S.VAR_DIFFICULTY) == difficulty, "reopening the selector cannot change difficulty")
        L.shot("difficulty_" .. difficulty .. "_confirmed")
        L.runHeader("DifficultySaveHeader")
        emu:reset()
        L.continueSave()
        L.expect(L.getFlag(S.FLAG_DIFFICULTY_CHOSEN), "choice survives actual save/reset/CONTINUE")
        L.expect(L.getVar(S.VAR_DIFFICULTY) == difficulty, "difficulty survives actual save/reset/CONTINUE")
        L.runHeader("DifficultyHermesHeader")
        local kerykos = "EmporionCity_TempleOfHermes_EventScript_Kerykos"
        local limit = ({150, 120, 100})[difficulty + 1]
        local function spokenLimit()
            local digits = tostring(limit)
            for i = 1, #digits do
                L.expect(emu:read8(S.gStringVar1 + i - 1) == S.CHAR_0 + tonumber(digits:sub(i, i)),
                         "Kerykos announces this difficulty's real step budget")
            end
            L.expect(emu:read8(S.gStringVar1 + #digits) == S.EOS, "the spoken step budget ends after its digits")
        end
        L.talk(L.npc(kerykos), {answers = {"no"}})
        spokenLimit()
        L.expect(L.getVar(S.VAR_TEMP_3) == 0, "declining the rite does not start the step-glass")
        local logText, captured = L.logText, false
        L.logText = function()
            logText()
            if not captured then
                L.wait(40)
                L.shot("difficulty_" .. difficulty .. "_repeat_budget")
                captured = true
            end
        end
        L.talk(L.npc(kerykos))
        L.logText = logText
        L.expect(captured, "the repeat instructions were actually shown")
        L.expect(L.getVar(S.VAR_TEMP_3) == 1 and L.getVar(S.VAR_TEMP_2) == limit,
                 "the real Herald's Run starts with this difficulty's budget")
        L.expect(L.getVar(S.VAR_TEMP_6) == limit // 2, "the native halfway warning is difficulty-aware")
        spokenLimit()
        local warnings = 0
        L.logText = function()
            warnings = warnings + 1
            logText()
            L.wait(40)
            L.shot("difficulty_" .. difficulty .. "_half_warning")
        end
        L.runHeader("DifficultyHalfGlassHeader")
        L.logText = logText
        L.expect(warnings == 1, "the native halfway tick actually displays its warning")
        L.expect(L.getVar(S.VAR_TEMP_2) == limit // 2 and L.idle(),
                 "the native halfway tick finishes and returns control")
        L.shot("difficulty_" .. difficulty .. "_half_glass")
    end
end)
