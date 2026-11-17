local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "thyrsa_symbols.lua")) do S.SCRIPTS[k] = v end
local T = "ThyrsaCity_TempleOfDionysus_EventScript_"
local A = "ThyrsaCity_Amphitheater_EventScript_"
local C = "ThyrsaCity_EventScript_"
local expect = L.expect

local function mask(prefix, role)
    L.talk(L.sign(prefix .. "Masks"), {menuChoice = role - 1})
    expect(L.getVar(S.VAR_MASK) == role, "the native mask menu selects role " .. role)
end

local function fullPocket()
    local pocket = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
    local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    local saved = {}
    for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
        saved[i] = {emu:read16(pocket + i * S.ITEM_SLOT_SIZE),
                    emu:read16(pocket + i * S.ITEM_SLOT_SIZE + 2) ~ key}
        emu:write16(pocket + i * S.ITEM_SLOT_SIZE, S.ITEM_TORCH)
        emu:write16(pocket + i * S.ITEM_SLOT_SIZE + 2, 1 ~ key)
    end
    return function()
        local live = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
        local liveKey = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
        for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
            emu:write16(live + i * S.ITEM_SLOT_SIZE, saved[i][1])
            emu:write16(live + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ liveKey)
        end
    end
end

L.start(function()
    L.quickstart()
    L.runHeader("Thyrsa_SetupHeader")
    L.setBeat("connected_roads", false)
    L.setFlag(S.FLAG_ACT1, false)
    L.go(45, 6, {trigger = true})
    L.settle()
    local _, y = L.pos()
    expect(y == 7, "the north gate still blocks departure before Act I closes")
    L.setFlag(S.FLAG_ACT1)
    for _, map in ipairs({S.MAP_R6, S.MAP_MOUNTAIN, S.MAP_R7, S.MAP_CITY}) do
        L.leaveEdge("up", map)
        expect(L.mapId() == map, "actual connected road crossing to map " .. map)
        L.shot("connected_" .. map)
    end
    L.useWarp(S.MAP_CLINIC)
    L.talk(L.npc("ThyrsaCity_Asclepeion_EventScript_Healer"))
    expect(L.idle(), "the real Thyrsa healer returns control")
    L.talk(L.sign("ThyrsaCity_Asclepeion_EventScript_Pithos"), {menuChoice = 2})
    expect(L.idle(), "the Thyrsa Pithos menu can be closed normally")
    L.shot("clinic")
    L.useWarp(S.MAP_CITY)
    L.useWarp(S.MAP_TEMPLE)
    L.setBeat("mask_trial", false)
    -- The Three-Act Play, solved from its clues: read them as a player would.
    for _, clue in ipairs({"Script", "Rules", "Costumes", "PanelRight", "Prompter"}) do
        local target = clue == "Prompter" and L.npc(T .. clue) or L.sign(T .. clue)
        L.talk(target, {every = clue == "Script"})
        expect(L.idle(), "the " .. clue .. " clue returns control")
    end
    L.talk(L.sign(T .. "Door1R"))
    expect(L.getVar(S.VAR_ACT) == 0, "no one walks on barefaced")
    -- Act I teaches: a wrong door or face costs nothing.
    mask(T, 2)
    L.talk(L.sign(T .. "Door1R"))
    expect(L.getVar(S.VAR_ACT) == 0 and select(2, L.pos()) >= 33, "Act I's wrong face is caught without penalty")
    mask(T, 1)
    L.talk(L.sign(T .. "Door1L"))
    expect(L.getVar(S.VAR_ACT) == 0 and select(2, L.pos()) >= 33, "Act I's wrong door is caught without penalty")
    L.talk(L.sign(T .. "Door1R"), {every = true})
    local x, y = L.pos()
    expect(L.getVar(S.VAR_ACT) == 1 and x == 18 and y == 30, "the stranger enters laughing from the harbor door")
    L.shot("act1_stage")
    -- Act II: the vintner, woken in his house. A wrong door drops you backstage.
    mask(T, 2)
    L.talk(L.sign(T .. "Door2L"))
    x, y = L.pos()
    expect(L.defeated(S.TRAINER_COMIC), "the comic acolyte is a checkpoint on Act I's stage")
    expect(L.mapId() == S.MAP_TEMPLE and L.getVar(S.VAR_ACT) == 1 and x == 12 and y == 36,
           "a wrong door in Act II drops through the trapdoor into the green room")
    L.shot("trapdoor")
    -- The right door in the wrong mask: the chorus fights you, every time.
    mask(T, 1)
    local battles = #L.battles
    L.talk(L.sign(T .. "Door2M"), {every = true})
    expect(#L.battles == battles + 1 and L.battles[#L.battles].trainerId == S.TRAINER_CHORUS
           and L.getVar(S.VAR_ACT) == 1, "the right door in the wrong mask means a chorus battle")
    mask(T, 1)
    battles = #L.battles
    L.talk(L.sign(T .. "Door2M"))
    expect(#L.battles == battles + 1 and L.battles[#L.battles].trainerId == S.TRAINER_CHORUS,
           "the chorus fights a wrong face again")
    mask(T, 2)
    L.talk(L.sign(T .. "Door2M"), {every = true})
    x, y = L.pos()
    expect(L.getVar(S.VAR_ACT) == 2 and x == 12 and y == 22, "the vintner enters weeping from his house")
    L.talk(L.sign(T .. "FrescoFollow"))
    L.talk(L.npc(T .. "Koryphaios"))
    -- Act III: the torn page. The satyr play follows the god in by his door.
    mask(T, 3)
    L.talk(L.sign(T .. "Door3R"), {every = true})
    x, y = L.pos()
    expect(L.getVar(S.VAR_ACT) == 3 and x == 18 and y == 14, "the goat-men follow the god in from the harbor")
    L.talk(L.sign(T .. "MechaneUp"), {every = true})
    x, y = L.pos()
    expect(L.defeated(S.TRAINER_SATYR) and x == 12 and y == 6, "past the satyr acolyte, the crane lifts you to the roof")
    L.shot("roof")
    -- The solved stage stays open: down the crane, out to heal, and back up.
    L.talk(L.sign(T .. "MechaneDown"), {answers = {"yes"}})
    L.useWarp(S.MAP_CITY)
    L.useWarp(S.MAP_CLINIC)
    L.talk(L.npc("ThyrsaCity_Asclepeion_EventScript_Healer"))
    L.useWarp(S.MAP_CITY)
    L.useWarp(S.MAP_TEMPLE)
    L.talk(L.sign(T .. "MechaneUp"))
    x, y = L.pos()
    expect(x == 12 and y == 6, "the opened doors lead from the green room back to the crane")
    expect(emu:saveStateFile(L.OUT .. "before_thespis.ss", 31), "saved the trial before Thespis")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.talk(L.npc(T .. "Thespis"))
    L.battleMode = nil
    expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST and not L.getFlag(S.FLAG_BADGE04),
           "losing the actual Thespis battle cannot award the Laurel")
    expect(L.mapId() == S.MAP_CLINIC, "Thespis whiteout returns to Thyrsa's safe clinic")
    L.shot("thespis_loss")
    expect(emu:loadStateFile(L.OUT .. "before_thespis.ss", 31), "restored the trial for the win branch")
    L.wait(30)
    L.waitUntil(L.idle, 600, "control after restoring the trial")
    L.talk(L.npc(T .. "Thespis"), {every = true})
    expect(L.defeated(S.TRAINER_THESPIS) and L.getFlag(S.FLAG_BADGE04), "real Thespis victory grants Laurel 4")
    expect(L.itemCount(S.ITEM_TM06) == 1, "Toxic scroll awarded")
    local favor = emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_DIONYSUS)
    local wine = L.itemCount(S.ITEM_WINE)
    L.talk(L.sign(T .. "Altar"), {answers = {1, 0}, every = true})
    expect(L.itemCount(S.ITEM_WINE) == wine - 1
           and emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.GOD_DIONYSUS) == favor + 10,
           "the actual Dionysus temple altar consumes Wine for double loved-offering Favor")
    L.shot("mask_laurel")
    local battles = #L.battles
    L.talk(L.npc(T .. "Thespis"))
    expect(#L.battles == battles and L.itemCount(S.ITEM_TM06) == 1, "Laurel and scroll do not replay")
    L.talk(L.sign(T .. "MechaneDown"), {answers = {"yes"}})
    local _, down = L.pos()
    expect(down == 9, "the crane sets you back down on Act III's stage")
    L.useWarp(S.MAP_CITY)
    expect(L.mapId() == S.MAP_CITY, "the opened doors lead back out through the green room")
    L.useWarp(S.MAP_THEATER)
    L.setBeat("dionysia", false)
    L.goTrigger(L.triggers(A .. "Performance"))
    L.settle({every = true})
    expect(L.getFlag(S.FLAG_WATCHED), "the four-scene tragedy plays through without losing control")
    L.talk(L.npc(A .. "Thespis"), {every = true})
    L.talk(L.sign(A .. "Program"))
    mask(A, 3)
    L.talk(L.sign(A .. "DoorRight"))
    expect(L.getVar(S.VAR_SATYR) == 0, "the satyr ending cannot skip the first two entrances")
    mask(A, 1)
    L.talk(L.sign(A .. "DoorLeft"), {every = true})
    expect(L.getVar(S.VAR_SATYR) == 1, "the vineyard fool frees the first audience block")
    mask(A, 2)
    L.talk(L.sign(A .. "DoorRight"))
    expect(L.getVar(S.VAR_SATYR) == 0, "a wrong cue lets the trance take the audience back")
    for i, door in ipairs({"DoorLeft", "DoorMiddle", "DoorRight"}) do
        mask(A, i)
        L.talk(L.sign(A .. door), {every = true})
        expect(L.getVar(S.VAR_SATYR) == i, "a real entrance frees audience block " .. i)
    end
    expect(L.getFlag(S.FLAG_BROKEN), "the satyr play breaks the staged tragedy")
    L.shot("theater_awake")
    L.useWarp(S.MAP_CITY)
    L.setBeat("silenos", false)
    L.talk(L.npc(C .. "Silenos"), {answers = {1, 0, 0, 2}})
    expect(not L.getFlag(S.FLAG_RIDDLE), "three wrong riddles leave the contest retryable")
    L.talk(L.npc(C .. "Silenos"), {answers = {1, 1}})
    expect(L.getFlag(S.FLAG_RIDDLE) and L.itemCount(S.ITEM_GIRDLE) == 0, "one distinct win is not enough")
    L.talk(L.npc(C .. "Silenos"), {answers = {1}})
    expect(L.itemCount(S.ITEM_GIRDLE) == 0, "repeating a won contest cannot count twice")
    L.talk(L.npc(C .. "Silenos"), {answers = {2}, every = true})
    expect(L.defeated(S.TRAINER_SILENOS) and L.getFlag(S.FLAG_BATTLE), "Silenos's native battle is the second win")
    local restore = fullPocket()
    L.talk(L.npc(C .. "Silenos"))
    expect(not L.getFlag(S.FLAG_GIRDLE) and L.getFlag(S.FLAG_RIDDLE) and L.getFlag(S.FLAG_BATTLE),
           "a full relic pocket preserves the wins without losing the Girdle")
    restore()
    L.talk(L.npc(C .. "Silenos"), {every = true})
    expect(L.getFlag(S.FLAG_GIRDLE) and L.itemCount(S.ITEM_GIRDLE) == 1, "room made: actual Girdle awarded")
    L.talk(L.npc(C .. "Silenos"))
    expect(L.itemCount(S.ITEM_GIRDLE) == 1, "the Girdle cannot be collected twice")
    L.runHeader("Thyrsa_SaveHeader")
    emu:reset()
    L.continueSave()
    expect(L.mapId() == S.MAP_CITY and L.getFlag(S.FLAG_BADGE04) and L.getFlag(S.FLAG_BROKEN)
           and L.getFlag(S.FLAG_GIRDLE) and L.itemCount(S.ITEM_GIRDLE) == 1,
           "chapter completion survives an actual save/reset/CONTINUE")
    L.shot("saved_chapter")
end)
