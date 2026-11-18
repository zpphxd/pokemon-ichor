-- Delphoi's chapter, walked (tools/ichor/tests/delphoi.sh): III-6A to III-8.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "delphoi_scripts.lua")) do S.SCRIPTS = S.SCRIPTS or {}; S.SCRIPTS[k] = v end

local function flag(f, text) L.expect(L.getFlag(f), text) end
local function act(n, text) L.expect(L.getVar(S.VAR_ICHOR_ACT3) == n, text .. " (VAR_ICHOR_ACT3 = " .. n .. ")") end
local function scene(script, receipt)
    for _ = 1, 6 do
        if L.getFlag(receipt) then return end
        if not L.goTrigger(L.triggers(script)) then L.settle({answers = {"yes", "yes", "yes"}}) end
        L.settle({answers = {"yes", "yes", "yes"}, limit = 60000})
    end
    L.expect(L.getFlag(receipt), "the scene finishes: " .. script)
end
-- surf from the bank onto water in direction `key`, then ride `n` steps that way
local function surfOff(key)
    L.face(key)
    L.tap(K.A)
    L.wait(10)
    L.settle({answers = {"yes"}})
    L.wait(30)
end
local function ride(key, n)
    local moved = 0
    for _ = 1, n + 6 do
        if moved >= n then break end
        local x0, y0 = L.pos()
        local r = L.step(key)
        if r == "taken" then L.settle({answers = {"yes"}}) end
        L.wait(20)
        local x1, y1 = L.pos()
        if x1 ~= x0 or y1 ~= y0 then moved = moved + 1 end
    end
end
-- climb the waterfall in front (the Horn of Achelous)
local function climb()
    L.face(K.UP)
    L.tap(K.A)
    L.wait(10)
    L.settle({answers = {"yes"}, limit = 30000})
    L.wait(60)
end
local function heal() L.runHeader("Delphoi_HealHeader") end
local function mirror(nth, turns)
    for _ = 1, turns do
        L.talk(L.npc("Delphoi_TempleOfApollo_EventScript_Mirror", nth), {answers = {"yes"}})
        L.settle({answers = {"yes"}})
    end
end

L.start(function()
    L.quickstart()
    L.runHeader("Delphoi_SetupHeader")
    L.assistLevel100()
    L.expect(L.mapId() == S.MAP_KIRRHA, "the chapter starts on Kirrha's east road")

    -- III-6A: Kirrha's east road onto the Sacred Olives; the Titans' column
    L.leaveEdge("right", S.MAP_OLIVES)
    L.expect(L.mapId() == S.MAP_OLIVES, "Kirrha's east road meets the Sacred Olives")
    scene("Route28_SacredOlives_EventScript_ColumnScene", S.FLAG_COLUMN)
    L.shot("olives_column")
    heal()
    L.go(43, 2)
    heal()
    L.leaveEdge("up", S.MAP_GORGE)
    L.expect(L.mapId() == S.MAP_GORGE, "the plain's east gate leads into the gorge")

    -- III-6B: the sentries, the camp, Agrios at the cutting
    scene("Route28_KastalianGorge_EventScript_Sentries", S.FLAG_SENTRIES)
    L.shot("gorge_camp")
    heal()
    L.go(13, 27, {avoid = {16, 28, 21, 33}})
    heal()
    L.go(13, 21)
    L.settle()
    L.expect(L.defeated(S.TRAINER_AGRIOS), "Gigas Agrios holds the cutting and is beaten")
    heal()
    L.go(10, 17)
    L.shot("gorge_herm")
    -- the lower fall: surf the plunge pool, climb, land on the middle ledge
    surfOff(K.LEFT)
    ride(K.LEFT, 2)
    climb()
    local x, y = L.pos()
    L.expect(y <= 13, string.format("the Horn climbs the lower fall (now at %d,%d)", x, y))
    ride(K.RIGHT, 3)
    L.go(11, 10)
    L.settle()
    heal()
    L.go(11, 10)
    L.expect(select(1, L.pos()) == 11, "on the pool's rim by Chrysis")
    -- the upper fall from the pool beside Chrysis
    surfOff(K.LEFT)
    ride(K.LEFT, 3)
    ride(K.UP, 1)
    climb()
    ride(K.UP, 2)
    ride(K.RIGHT, 7)
    L.go(13, 1)
    L.leaveEdge("up", S.MAP_DELPHOI)
    L.expect(L.mapId() == S.MAP_DELPHOI, "the top of the falls is Delphoi")

    -- III-6C: the first sight (the camera climbs the Sacred Way to the temple
    -- under the Phaedriades), then the Pythia passes
    if L.goTrigger(L.triggers("Delphoi_EventScript_Arrival")) then L.wait(1) end
    L.wait(560)
    L.shot("delphoi_arrival_pan")
    scene("Delphoi_EventScript_Arrival", S.FLAG_ARRIVED)
    act(11, "Delphoi is reached")
    L.shot("delphoi_arrival")

    -- III-6D: the Pythian Light
    heal()
    L.go(23, 13)
    L.useWarp(S.MAP_TEMPLE)
    L.expect(L.mapId() == S.MAP_TEMPLE, "the temple's door under KNOW THYSELF")
    L.wait(30)
    mirror(1, 1)
    flag(S.FLAG_DISC_0, "teach: one turn of M1 lights disc 0")
    L.go(9, 39)
    L.settle()
    mirror(2, 2)
    flag(S.FLAG_DISC_1, "chamber 1: M2 lights disc 1")
    L.shot("temple_chamber1")
    L.go(9, 32)
    heal()
    mirror(3, 1)
    flag(S.FLAG_DISC_2, "chamber 2: M3 lights disc 2")
    mirror(3, 2)
    mirror(4, 1)
    L.go(5, 25)
    mirror(5, 1)
    mirror(6, 3)
    flag(S.FLAG_DISC_3, "chamber 3: round the serpent, M5 lights disc 3")
    mirror(6, 2)
    L.go(2, 17)
    mirror(7, 3)
    mirror(8, 2)
    flag(S.FLAG_DISC_4, "chamber 4: M7 lights disc 4 at the stair head")
    L.settle()
    L.shot("temple_chamber4")
    heal()
    L.go(12, 10)
    mirror(9, 1)
    flag(S.FLAG_BRAZIER, "master: M8 focuses the beam on the brazier")
    L.talk(L.sign("Delphoi_TempleOfApollo_EventScript_Brazier"))
    L.settle()
    local vents = {}
    for vx = 5, 13 do vents[vx .. ",7"] = true end
    for vx = 1, 17 do if vx ~= 7 then vents[vx .. ",5"] = true end end
    heal()
    L.go(8, 4, {avoid = vents})
    L.face(K.UP)
    L.tap(K.A)
    L.settle({limit = 120000})
    flag(S.FLAG_LIGHT_DONE, "the carried fire lights the tripod")
    L.expect(L.defeated(S.TRAINER_PHEMONOE), "the Pythia battles on the tripod")
    flag(S.FLAG_BADGE08_GET, "the Sun Laurel")
    flag(S.FLAG_CORVUS, "Corvus joins the Star Chart")
    L.expect(L.itemCount(S.ITEM_TM_FIRE) == 1, "the Pythia gives TM Mystical Fire")
    flag(S.FLAG_SPOKE, "the Pythia says a whole sentence")
    act(12, "the Sun Laurel")
    L.shot("sun_laurel")

    -- III-7: Mom at the Kastalian spring
    L.go(9, 45)
    L.useWarp(S.MAP_DELPHOI)
    scene("Delphoi_EventScript_MomScene", S.FLAG_MOM)
    L.expect(L.itemCount(S.ITEM_HONEY_JAR) == 1, "Mom gives Melitta's Honey")
    act(13, "Mom at the spring")
    L.shot("mom_spring")

    -- III-8: the Omphalos at night
    heal()
    scene("Delphoi_EventScript_OmphalosNight", S.FLAG_NIGHT)
    L.expect(L.defeated(S.TRAINER_EPHIALTES) and L.defeated(S.TRAINER_THOAS),
             "Rhea beside you, the two Gigas are beaten")
    flag(S.FLAG_OPEN, "the Omphalos is open")
    act(14, "the Omphalos opens")
    L.expect(L.mapId() == S.MAP_STAIR, "the stair goes down from the stone (the climax's handoff)")
    L.shot("omphalos_stair")
    L.runHeader("Delphoi_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.mapId() == S.MAP_STAIR and L.getFlag(S.FLAG_BADGE08_GET) and L.getVar(S.VAR_ICHOR_ACT3) == 14,
             "the chapter's end survives save/reset/CONTINUE")
end)
