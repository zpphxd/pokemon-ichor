-- Knossa above ground, played through (design/phase4/SCRIPT.md III-3A to III-3E,
-- III-3O, III-3P's landing, III-4): Kythera's crossing lands at Amnisos, the
-- arrival, the Asclepeion and Kydon, the Bull Road and Milon's practice leap,
-- the North Entrance, Ariadne, the first leap, the Thread; then, standing in for
-- the Labyrinth chapters, the court at night (Scene K, Alethea, the Megaron),
-- the dawn landing, Asterion, Alethea's gull, Daphne's letter and boarding.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "knossa_scripts.lua")) do S.SCRIPTS[k] = v end
local function flag(f, text) L.expect(L.getFlag(f), text) end
local function knossa() return L.getVar(S.VAR_KNOSSA) end

-- A bull-leap, timed: read the line from the lane's end facing the bull, say yes,
-- and press A the moment the bull's head starts across the line.
local function leap(lineScript, bullScript, lineX, lineY, receipt)
    for try = 1, 6 do
        if L.getFlag(receipt) then return try end
        L.go(lineX, lineY + 1)
        L.face(K.UP)
        L.tap(K.A)
        local bull = L.npc(bullScript)
        L.settle({answers = {"yes"}, stop = function()
            local _, y = L.objectAt(bull.localId)
            return y ~= nil and y > bull.y
        end})
        for _ = 1, 400 do
            local _, y = L.objectAt(bull.localId)
            if y == lineY then break end
            L.wait(1)
        end
        L.wait(2)
        L.tap(K.A)
        L.settle({answers = {"no"}})
    end
    L.expect(L.getFlag(receipt), "a timed press makes a clean leap")
end

L.start(function()
    L.quickstart()
    L.runHeader("Knossa_SetupHeader")
    L.assistLevel100()

    -- III-1I to III-3A: the crossing, and Alethea on the quay at dawn
    L.talk(L.npc("KytheraSkandeia_EventScript_Nausikles"), {answers = {"yes"}})
    L.settle()
    L.expect(L.mapId() == S.MAP_AMNISOS, "Nausikles sails to Amnisos")
    flag(S.FLAG_ARRIVED, "the arrival scene plays on the quay")
    L.expect(L.getVar(S.VAR_ICHOR_ACT3) == 5 and knossa() == 1, "landing sets VAR_ICHOR_ACT3 5 and VAR_ICHOR_KNOSSA 1")
    L.shot("amnisos_arrival")
    L.useWarp(S.MAP_AM_CLINIC)
    L.talk(L.npc("KnossaAmnisos_Asclepeion_EventScript_Akestor"))
    L.expect(L.lastHeal() == S.MAP_AMNISOS, "Amnisos's Asclepeion becomes the respawn")
    L.useWarp(S.MAP_AMNISOS)
    L.useWarp(S.MAP_KYDON)
    local honey = L.itemCount(S.ITEM_HONEY)
    L.talk(L.npc("KnossaAmnisos_KydonsHouse_EventScript_Kydon"))
    flag(S.FLAG_HONEY, "Kydon gives his thyme honey")
    L.expect(L.itemCount(S.ITEM_HONEY) == honey + 3, "three jars")
    L.useWarp(S.MAP_AMNISOS)
    L.shot("amnisos_town")

    -- III-3B: the Bull Road, Milon's practice leap, to the palace
    L.go(19, 29)
    L.leaveEdge("down", S.MAP_BULL_ROAD)
    L.expect(L.mapId() == S.MAP_BULL_ROAD, "Amnisos's south gap opens on the Bull Road")
    L.shot("bull_road_north")
    L.talk(L.npc("KnossaBullRoad_EventScript_Milon"))
    leap("KnossaBullRoad_EventScript_MilonsLine", "KnossaBullRoad_EventScript_Herd", 15, 31, S.FLAG_MILON)
    flag(S.FLAG_MILON, "Milon's practice leap lands clean")
    L.shot("bull_road_herd")
    L.useWarp(S.MAP_HUT)
    L.talk(L.npc("KnossaBullRoad_Hut_EventScript_Bombylia"))
    L.useWarp(S.MAP_BULL_ROAD)
    L.go(15, 48)
    L.leaveEdge("down", S.MAP_PALACE)
    L.expect(L.mapId() == S.MAP_PALACE, "the Bull Road reaches the palace")

    -- III-3C: the North Entrance
    L.go(29, 14)
    L.expect(knossa() == 2, "beating Keramos and Gypsos opens the North Entrance")
    L.shot("palace_court")

    -- III-3D: the Throne Room, Ariadne (Scene A)
    L.useWarp(S.MAP_THRONE)
    L.talk(L.npc("KnossaPalace_ThroneRoom_EventScript_Ariadne"))
    flag(S.FLAG_MET_ARIADNE, "Scene A plays")
    L.expect(knossa() == 3, "Scene A sets VAR_ICHOR_KNOSSA 3")
    L.useWarp(S.MAP_PALACE)

    -- III-3E: Sarpedon, the first leap, and the Thread (Scene B)
    L.talk(L.npc("KnossaPalace_EventScript_Sarpedon"))
    leap("KnossaPalace_EventScript_LeapLine", "KnossaPalace_EventScript_GentleBull", 30, 26, S.FLAG_FIRST_LEAP)
    L.expect(knossa() == 4, "the first clean leap sets VAR_ICHOR_KNOSSA 4")
    L.shot("first_leap")
    L.useWarp(S.MAP_STAIR)
    L.talk(L.npc("KnossaPalace_GrandStaircase_EventScript_Ariadne"))
    flag(S.FLAG_THREAD, "Ariadne gives the Thread")
    L.expect(L.itemCount(S.ITEM_THREAD) == 1 and knossa() == 5, "the Thread is in the bag; VAR_ICHOR_KNOSSA 5")
    L.shot("grand_staircase")

    -- III-3O: the court at night after the Turning (Scene K), Alethea, the Megaron
    L.runHeader("Knossa_TurningHeader")
    L.settle()
    L.talk(L.npc("KnossaPalace_EventScript_Kleon"), {answers = {"yes", "yes"}})
    L.settle()
    flag(S.FLAG_KLEON, "Scene K: Kleon reads the tablet and goes")
    flag(S.FLAG_TOLD, "Alethea hears about Phaedon")
    L.expect(L.mapId() == S.MAP_MEGARON, "the night passes in the Queen's Megaron")
    flag(S.FLAG_WOKE, "Ariadne wakes you before dawn")
    L.shot("megaron_before_dawn")

    -- III-3P: the landing from the Icarus Shaft, Asterion, Alethea's gull
    L.runHeader("Knossa_IcarusHeader")
    L.settle()
    L.expect(L.getVar(S.VAR_ICHOR_ACT3) == 6, "the dawn landing sets VAR_ICHOR_ACT3 6")
    L.shot("court_at_dawn")
    L.talk(L.npc("KnossaPalace_EventScript_Asterion"), {answers = {"yes"}})
    flag(S.FLAG_ASTERION, "Asterion steps into the ball")
    L.talk(L.npc("KnossaPalace_EventScript_AletheaNight"))
    flag(S.FLAG_DAWN, "Alethea sends her gull and goes down to the quay")

    -- III-4: evening on Amnisos's quay: Daphne's letter, and boarding for Gytheion
    L.runHeader("Knossa_EveningHeader")
    L.settle({answers = {"yes"}})
    flag(S.FLAG_LETTER, "Daphne's letter is read on the quay")
    flag(S.FLAG_GYTHEION, "the chapter ends boarding for Gytheion")
    L.expect(knossa() == 20, "boarding sets VAR_ICHOR_KNOSSA 20")
    -- the seam into Lakonia: the Euploia's deck plays III-5A and lands at Gytheion
    L.settle()
    L.expect(L.mapId() == S.MAP_GYTHEION and L.getFlag(S.FLAG_ARRIVED_GYTHEION),
        "the Euploia's deck carries on to Gytheion (Lakonia's III-5A)")
    L.shot("landed_at_gytheion")
end)
