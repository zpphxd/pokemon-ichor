local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K = L.S, L.K
local emu = L.emu
for k, v in pairs(dofile(L.OUT .. "approach_symbols.lua")) do S.SCRIPTS[k] = v end
S.SCRIPTS.EventScript_StrengthBoulder = S.EventScript_StrengthBoulder
local function cross(dir, map, name)
    L.leaveEdge(dir, map)
    L.expect(L.mapId() == map, "actual connected crossing: " .. name)
    L.shot(name)
end
local function ferry(source, dest, destination, save)
    L.talk(L.npc(source .. "_EventScript_Captain"))
    L.expect(L.mapId() == S.MAP_FERRY and L.getVar(S.VAR_GULF_DEST) == destination,
             "boarded the real trireme from " .. source)
    L.shot("gulf_deck")
    if save then
        L.runHeader("Approach_SaveHeader")
        L.emu:reset()
        L.continueSave()
        L.expect(L.mapId() == S.MAP_FERRY and L.getVar(S.VAR_GULF_DEST) == destination,
                 "the correct destination survives save/reset aboard the trireme")
    end
    L.talk(L.npc("GulfTrireme_EventScript_Captain"))
    L.expect(L.mapId() == dest, "landed at the correct Gulf harbor")
end
L.start(function()
    L.quickstart()
    L.runHeader("Approach_SetupHeader")
    L.setBeat("kopais_and_parnassos", false)
    cross("left", S.MAP_R8, "kopais")
    cross("left", S.MAP_LEBADEIA, "lebadeia")
    L.talk(L.npc("Lebadeia_EventScript_Healer"))
    L.expect(L.idle(), "Lebadeia's actual healer returns control")
    cross("down", S.MAP_R9, "parnassos")
    cross("down", S.MAP_KIRRHA, "kirrha")
    L.setBeat("gulf_crossing", false)
    ferry("Kirrha", S.MAP_AIGION, 0, true)
    ferry("Aigion", S.MAP_KIRRHA, 1)
    ferry("Kirrha", S.MAP_AIGION, 0)
    L.talk(L.npc("Aigion_EventScript_Healer"))
    cross("down", S.MAP_R11, "drum_pass")
    L.expect(emu:saveStateFile(L.OUT .. "before_drum_pass.ss", 31), "saved the journey before the loss branch")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.talk(L.npc("Route11_DrumPass_EventScript_DORYS"))
    L.battleMode = nil
    L.expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST
             and L.mapId() == S.MAP_AIGION, "a real pass whiteout returns to Aigion's outdoor healer")
    L.expect(L.canReachNextTo(19, 26), "the outdoor recovery point has a walkable route back to the ferry")
    L.shot("aigion_recovery")
    L.expect(emu:loadStateFile(L.OUT .. "before_drum_pass.ss", 31), "restored the pass for onward travel")
    L.wait(30)
    L.waitUntil(L.idle, 600, "control after restoring the journey")
    L.setBeat("girdle_gate", false)
    L.go(11, 23)
    L.talk(L.npc("EventScript_StrengthBoulder"))
    L.tap(K.DOWN, 8)
    L.wait(40)
    local _, y = L.pos()
    L.expect(y == 23 and L.itemCount(S.ITEM_GIRDLE) == 0,
             "the real column drum blocks the pass without the Girdle")
    L.runHeader("Approach_GirdleHeader")
    L.talk(L.npc("EventScript_StrengthBoulder"))
    for _ = 1, 7 do L.tap(K.DOWN, 8); L.wait(48) end
    _, y = L.pos()
    L.expect(y >= 26, "the native Girdle/Strength action pushes the actual column drum")
    L.shot("girdle_pass")
    cross("down", S.MAP_STYX, "styx_falls")
    L.talk(L.npc("StyxFalls_EventScript_Guide"))
    cross("down", S.MAP_R12, "cypress_road")
    cross("down", S.MAP_ARKADIA, "arkadia")
    L.talk(L.npc("Arkadia_EventScript_Healer"))
    L.runHeader("Approach_SaveHeader")
    L.emu:reset()
    L.continueSave()
    L.expect(L.mapId() == S.MAP_ARKADIA and L.itemCount(S.ITEM_GIRDLE) == 1,
             "the connected journey and relic survive actual save/reset/CONTINUE")
    L.shot("saved_arkadia")
end)
