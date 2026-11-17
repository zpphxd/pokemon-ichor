local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local routes = dofile("tools/ichor/tests/act3_galatea_routes.lua")
local keys = {N = K.UP, S = K.DOWN, W = K.LEFT, E = K.RIGHT}
for k, v in pairs(dofile(L.OUT .. "kythera_scripts.lua")) do S.SCRIPTS[k] = v end
local function flag(f, text) L.expect(L.getFlag(f), text) end
local function favor(god) return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + god) end
local function scene(script, receipt)
    for _ = 1, 5 do
        if L.getFlag(receipt) then return end
        if not L.goTrigger(L.triggers(script)) then L.settle() end
    end
    L.expect(L.getFlag(receipt), "the connected scene finishes: " .. script)
end
local function walk(route)
    for _, action in ipairs(route.steps) do
        if action:sub(1, 1) == "t" then
            local x, y = L.objectAt(S[action:sub(2)])
            local px, py = L.pos()
            L.face(x > px and K.RIGHT or x < px and K.LEFT or y > py and K.DOWN or K.UP)
            L.tap(K.A)
            L.wait(10)
            L.settle({answers = {"yes"}})
        else
            local result = L.step(keys[action])
            if result == "blocked" then L.fail("the connected Gallery route is blocked") end
            if result == "taken" then L.settle({answers = {"yes"}}) end
        end
    end
    local x, y = L.pos()
    L.shot("gallery_room_" .. route.endy)
    L.expect(x == route.endx and y == route.endy,
             string.format("the connected Gallery room ends at (%d,%d), expected (%d,%d)", x, y, route.endx, route.endy))
end
local function fillKeys()
    local saved = {}
    local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    local pocket = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
    for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
        local slot = pocket + i * S.ITEM_SLOT_SIZE
        saved[i] = {emu:read16(slot), emu:read16(slot + 2) ~ key}
        emu:write16(slot, S.ITEM_HORN + 1)
        emu:write16(slot + 2, 1 ~ key)
    end
    return function()
        local p = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
        local k = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
        for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
            emu:write16(p + i * S.ITEM_SLOT_SIZE, saved[i][1])
            emu:write16(p + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ k)
        end
    end
end
L.start(function()
    L.quickstart()
    L.runHeader("Kythera_SetupHeader")
    L.assistLevel100()
    L.talk(L.npc("Kaldera_EventScript_Nausikles"), {menuChoice = 4})
    L.expect(L.mapId() == S.MAP_DECK and L.getVar(S.VAR_DEST) == 5,
             "Kaldera boards the real Kythera voyage")
    L.runHeader("Kythera_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.mapId() == S.MAP_DECK and L.getVar(S.VAR_DEST) == 5,
             "the Kythera destination survives save/reset/CONTINUE")
    L.talk(L.npc("TriremeDeck_EventScript_Nausikles"), {answers = {"yes"}})
    L.expect(L.mapId() == S.MAP_SKANDEIA, "the captain makes port at Skandeia")
    flag(S.FLAG_KEPT, "the actual requisition battle keeps the Euploia")
    L.shot("skandeia_arrival")
    scene("KytheraSkandeia_EventScript_AletheaRejoins", S.FLAG_REJOINED)
    flag(S.FLAG_REJOINED, "Alethea actually rejoins on the street")
    local zeus = favor(S.GOD_ZEUS)
    L.useWarp(S.MAP_AXYLOS, true)
    L.settle({answers = {"yes"}, limit = 40000})
    flag(S.FLAG_GUESTS, "the bad guests leave after the actual double battle")
    L.expect(favor(S.GOD_ZEUS) == zeus + 5, "defending the host earns Zeus's Favor")
    L.shot("axylos_table")
    L.useWarp(S.MAP_SKANDEIA)
    L.useWarp(S.MAP_CLINIC)
    L.settle()
    local map = L.lastHeal()
    L.expect(map == S.MAP_SKANDEIA, "the island's real Asclepeion becomes the respawn")
    L.talk(L.npc("KytheraSkandeia_Asclepeion_EventScript_Healer"))
    L.useWarp(S.MAP_SKANDEIA)
    L.go(1, 16)
    L.leaveEdge("left", S.MAP_FOAM_ROAD)
    L.expect(L.mapId() == S.MAP_FOAM_ROAD, "the harbor connects to the Foam Road")
    L.go(30, 8)
    scene("KytheraFoamRoad_EventScript_AletheaRock", S.FLAG_SHERD)
    flag(S.FLAG_SHERD, "Alethea's actual excavation finds the Paris sherd")
    L.go(41, 1)
    L.leaveEdge("up", S.MAP_SPRING)
    scene("KytheraSpringOfKallirhoe_EventScript_AletheaScene", S.FLAG_SPRING)
    flag(S.FLAG_SPRING, "the Spring of Kallirhoe scene plays")
    L.shot("kallirhoe")
    L.leaveEdge("down", S.MAP_FOAM_ROAD)
    L.go(4, 8)
    L.leaveEdge("left", S.MAP_PAPHIA)
    scene("KytheraPaphia_EventScript_AletheaSails", S.FLAG_SAILED)
    flag(S.FLAG_SAILED, "Alethea actually takes the honey boat")
    L.useWarp(S.MAP_PAPHIA_CLINIC)
    L.talk(L.npc("KytheraPaphia_Asclepeion_EventScript_Healer"))
    L.useWarp(S.MAP_PAPHIA)
    L.useWarp(S.MAP_TEMPLE)
    L.go(routes.pronaos.x, routes.pronaos.y)
    local caught = false
    for _, action in ipairs(routes.pronaos_back.steps) do
        local x, y = L.pos()
        if L.step(keys[action]) == "taken" then L.settle() end
        local nx, ny = L.pos()
        if math.abs(nx - x) + math.abs(ny - y) > 1 then caught = true; break end
    end
    local x, y = L.pos()
    L.expect(caught and x == 5 and y == 34, "a real failed attempt resets the first room at its door")
    local aphrodite = favor(S.GOD_APHRODITE)
    walk(routes.pronaos)
    walk(routes.gallery)
    if L.step(K.UP) == "taken" then L.settle() end
    walk(routes.court)
    flag(S.FLAG_BADGE07_GET, "the connected chapter earns the Foam Laurel")
    L.expect(L.itemCount(S.ITEM_TM) == 1, "Galatea actually gives Dazzling Gleam")
    L.expect(favor(S.GOD_APHRODITE) == aphrodite + 15, "the Laurel grants Aphrodite's Favor")
    L.talk(L.npc("KytheraTempleOfAphrodite_EventScript_Galatea"))
    L.expect(L.itemCount(S.ITEM_TM) == 1 and favor(S.GOD_APHRODITE) == aphrodite + 15,
             "talking again duplicates neither the scroll nor Laurel Favor")
    L.shot("foam_laurel")
    L.useWarp(S.MAP_PAPHIA)
    L.useWarp(S.MAP_PAPHIA_CLINIC)
    L.talk(L.npc("KytheraPaphia_Asclepeion_EventScript_Healer"))
    L.useWarp(S.MAP_PAPHIA)
    L.go(30, 2)
    L.leaveEdge("up", S.MAP_FALLS)
    L.useWarp(S.MAP_MILL)
    L.useWarp(S.MAP_FALLS)
    local krenaia = "KytheraNeraidaFalls_EventScript_Krenaia"
    L.talk(L.npc(krenaia), {answers = {"yes"}})
    L.expect(not L.getFlag(S.FLAG_GOT_HORN), "insufficient First Fruits grant no Horn")
    L.talk(L.npc("BerryTreeScript", 1), {answers = {"yes"}})
    L.talk(L.npc("BerryTreeScript", 2), {answers = {"yes"}})
    local function berries() return L.itemCount(S.ITEM_LUM) + L.itemCount(S.ITEM_SITRUS) end
    local fruit = berries()
    L.expect(fruit >= 3, "the actual terrace trees provide enough First Fruits")
    L.talk(L.npc(krenaia), {answers = {"no"}})
    L.expect(berries() == fruit and not L.getFlag(S.FLAG_GOT_HORN), "declining keeps the fruit")
    local restore = fillKeys()
    L.talk(L.npc(krenaia), {answers = {"yes"}})
    L.expect(berries() == fruit and not L.getFlag(S.FLAG_GOT_HORN),
             "a full Key Items pocket refuses before consuming fruit")
    restore()
    L.talk(L.npc(krenaia), {answers = {"yes"}})
    L.expect(L.getFlag(S.FLAG_GOT_HORN) and L.itemCount(S.ITEM_HORN) == 1
             and berries() == fruit - 3 and L.getVar(S.VAR_ICHOR_ACT3) == 4,
             "exactly three harvested berries earn the actual Horn and advance the story")
    L.shot("river_awake")
    L.talk(L.npc(krenaia))
    L.expect(berries() == fruit - 3 and L.itemCount(S.ITEM_HORN) == 1, "the Horn cannot be claimed twice")
    L.runHeader("Kythera_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.getFlag(S.FLAG_GOT_HORN) and L.itemCount(S.ITEM_HORN) == 1
             and L.getFlag(S.FLAG_BADGE07_GET), "the completed chapter survives save/reset/CONTINUE")
end)
