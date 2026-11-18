-- The Sacred Way, walked (tools/ichor/maps/sacredway.py): Eleusa's east gate over
-- Route 15, Daphni and Route 16 to Astyra's gate, with a save and CONTINUE in Daphni.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "sacredway_scripts.lua")) do S.SCRIPTS[k] = v end
S.SCRIPTS.EventScript_StrengthBoulder = S.EventScript_StrengthBoulder
local function flag(f, text) L.expect(L.getFlag(f), text) end
local function beaten(t, who) flag(S.TRAINER_FLAGS_START + t, who .. " is beaten") end
local function heal() L.runHeader("SacredWay_HealHeader") end

L.start(function()
    L.quickstart()
    L.runHeader("SacredWay_SetupHeader")
    L.assistLevel100()
    L.settle()
    L.expect(L.mapId() == S.MAP_ELEUSA, "the test starts at Eleusa's east gate")

    -- Eleusa -> Route 15: the gate road, the causeway between the salt lakes
    L.leaveEdge("right", S.MAP_R15)
    L.expect(L.mapId() == S.MAP_R15, "Eleusa's east gate opens onto Route 15")
    L.shot("r15_gate")
    L.go(23, 16)
    beaten(S.TRAINER_TIMON, "Timon, at the gate,")
    beaten(S.TRAINER_HEGESO, "Hegeso, on the causeway,")
    L.shot("r15_causeway")
    heal()
    -- up the scarp stair, along the terrace, the herm and the spring
    L.go(48, 6)
    beaten(S.TRAINER_POLEMON, "Polemon, at the stair head,")
    beaten(S.TRAINER_PHILA, "Phila, past band 2,")
    L.talk(L.sign("Route15_MysteryRoad_EventScript_Herm"), {answers = {1}})
    L.talk(L.npc("Route15_MysteryRoad_EventScript_SpringKeeper"))
    L.shot("r15_spring")
    -- the shrine court: brace the Girdle, both drums onto their plates
    L.talk(L.npc("EventScript_StrengthBoulder"))
    for _, push in ipairs({ { 50, 9, K.RIGHT }, { 50, 9, K.LEFT }, { 49, 9, K.LEFT }, { 51, 9, K.RIGHT } }) do
        L.go(push[1], push[2])
        L.face(push[3])
        L.tap(push[3], 8)
        L.wait(48)
        L.settle()
    end
    L.go(52, 9)
    L.settle()
    flag(S.FLAG_SEAL, "both drums on the shrine court's plates open the stair down")
    L.shot("r15_seal_open")
    L.talk(L.ball(S.FLAG_HOLLOW))
    flag(S.FLAG_HOLLOW, "Kore's hollow, down the opened stair, pays its jar")
    heal()
    -- down the east stair, Agis, band 3, Praxon, into Daphni
    L.go(70, 18)
    beaten(S.TRAINER_AGIS, "Agis, on the east side of the pass,")
    beaten(S.TRAINER_PRAXON, "Praxon, above Daphni,")
    L.leaveEdge("right", S.MAP_DAPHNI)
    L.expect(L.mapId() == S.MAP_DAPHNI, "Route 15 comes down into Daphni")
    L.shot("daphni_west")

    -- Daphni: the healer registers the herm; the prayer laurel; the priestess
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.talk(L.npc("Daphni_EventScript_Healer"))
    L.expect(emu:read16(L.partyMon(0) + S.OFF_MON_HP) > 1, "Daphni's healer heals the party")
    flag(S.FLAG_TOWN_HERM, "the healer registers Daphni's travel herm")
    L.talk(L.sign("Daphni_EventScript_Laurel"), {answers = {0}})
    flag(S.FLAG_CORD, "the Sickle cuts the cord from the prayer laurel")
    L.useWarp(S.MAP_SANCTUARY)
    L.talk(L.npc("Daphni_Sanctuary_EventScript_Priestess"))
    flag(S.FLAG_CROWN, "the priestess gives the laurel crown for the freed laurel")
    L.shot("daphni_sanctuary")
    L.useWarp(S.MAP_DAPHNI)

    -- save on the laurel walk, at the cell an existing save stands on, reset, CONTINUE
    L.go(9, 10)
    L.runHeader("SacredWay_SaveHeader")
    emu:reset()
    L.continueSave()
    local x, y = L.pos()
    L.expect(L.mapId() == S.MAP_DAPHNI and x == 9 and y == 10, "CONTINUE resumes on Daphni's laurel walk at (9,10)")
    L.expect(L.getFlag(S.FLAG_TOWN_HERM) and L.getFlag(S.FLAG_SEAL) and L.getFlag(S.FLAG_CROWN),
             "the herm, the opened seal and the crown survive save/reset/CONTINUE")
    L.shot("daphni_continue")

    -- Route 16: the ford, the Kerameikos, the climb, the lookout, Astyra's gate
    L.leaveEdge("right", S.MAP_R16)
    L.expect(L.mapId() == S.MAP_R16, "Daphni's east road runs on to Route 16")
    heal()
    L.go(30, 17)
    beaten(S.TRAINER_NIKIAS, "Nikias, at Daphni's foot,")
    beaten(S.TRAINER_TIMARETE, "Timarete, before the ford,")
    L.shot("r16_ford")
    heal()
    L.go(47, 12)
    beaten(S.TRAINER_DIOTIMA, "Diotima, by the Akademia,")
    beaten(S.TRAINER_ARISTON, "Ariston, at the scarp stair,")
    heal()
    L.go(62, 11)
    beaten(S.TRAINER_STRATON, "Straton, on the terrace,")
    flag(S.FLAG_VIEW, "the lookout shows the Akropolis the first time")
    L.shot("r16_lookout")
    L.leaveEdge("right", S.MAP_ASTYRA)
    L.expect(L.mapId() == S.MAP_ASTYRA, "Route 16 reaches Astyra's gate")
    L.shot("astyra_gate")
end)
