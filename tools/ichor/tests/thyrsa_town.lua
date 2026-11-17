-- Thyrsa's ported city: doors both ways, the two roads, the houses' gifts.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S = L.S
for k, v in pairs(dofile(L.OUT .. "thyrsa_town_symbols.lua")) do S.SCRIPTS[k] = v end
local expect = L.expect
local C = "ThyrsaCity_EventScript_"

-- Through the door to `map` and back: the return lands on the tile below the door.
local function door(map, name, inside)
    L.useWarp(map)
    expect(L.mapId() == map, "the " .. name .. " door opens")
    L.shot(name)
    if inside then inside() end
    L.useWarp(S.MAP_CITY)
    expect(L.mapId() == S.MAP_CITY, "the " .. name .. " returns to Thyrsa")
    local x, y = L.pos()
    local ok = false
    for _, w in ipairs(L.mapEvents().warps) do
        if w.map == map and w.x == x and w.y + 1 == y then ok = true end
    end
    expect(ok, string.format("the %s returns in front of its own door (%d,%d)", name, x, y))
end

L.start(function()
    L.quickstart()
    L.runHeader("ThyrsaTown_SetupHeader")
    expect(L.mapId() == S.MAP_CITY, "arrived inside the Elektran Gate")
    L.shot("elektran_gate")
    L.talk(L.npc(C .. "Manto"))
    expect(L.getFlag(S.FLAG_MET_MANTO), "Manto on the Kadmeia wall")
    L.shot("kadmeia")
    door(S.MAP_CLINIC, "asclepeion")
    door(S.MAP_AGORA, "agora")
    door(S.MAP_TEMPLE, "temple")
    door(S.MAP_THEATER, "amphitheater")
    door(S.MAP_TAVERN, "tavern")
    door(S.MAP_MASKS, "mask_workshop")
    door(S.MAP_ACTOR, "actor_house")
    door(S.MAP_EUDORA, "eudora_house", function()
        L.talk(L.sign("ThyrsaCity_EudoraHouse_EventScript_TurnedEarth"), {answers = {"yes"}})
        expect(L.getFlag(S.FLAG_FIG_DUG), "the fig gives up the arm-ring")
        L.talk(L.npc("ThyrsaCity_EudoraHouse_EventScript_Eudora"))
        expect(L.getFlag(S.FLAG_BRACER) and L.itemCount(S.ITEM_POWER_BRACER) == 1, "Eudora gives the Power Bracer")
    end)
    door(S.MAP_MANTO, "manto_house", function()
        L.talk(L.npc("ThyrsaCity_MantoHouse_EventScript_Manto"))
        expect(L.getFlag(S.FLAG_MANTO_CROWS), "Manto asks about the crows")
    end)
    door(S.MAP_PINDAROS, "pindaros_house", function()
        local sprigs = L.itemCount(S.ITEM_LAUREL_SPRIG)
        L.talk(L.npc("ThyrsaCity_PindarosHouse_EventScript_Pindaros"), {menuChoice = 4})
        expect(L.getVar(S.VAR_LAURELS) == 4 and L.itemCount(S.ITEM_LAUREL_SPRIG) == sprigs + 1,
               "Pindaros hears about four laurels and gives a sprig")
        expect(L.idle(), "Pindaros's rest offer returns control")
    end)
    door(S.MAP_SOWN, "sown_house", function()
        L.talk(L.npc("ThyrsaCity_SownHouse_EventScript_Chthonia"))
        expect(L.getFlag(S.FLAG_FANG) and L.itemCount(S.ITEM_DRAGON_FANG) == 1, "Chthonia gives the Dragon Fang")
    end)
    door(S.MAP_VINTNER, "vintner_house", function()
        L.talk(L.npc("ThyrsaCity_VintnerHouse_EventScript_Staphylos"))
        expect(L.getFlag(S.FLAG_NUGGET) and L.itemCount(S.ITEM_NUGGET) >= 1, "Staphylos gives the press's Nugget")
    end)
    L.shot("square")
    L.leaveEdge("left", S.MAP_R8)
    expect(L.mapId() == S.MAP_R8, "the Neistan Gate crosses onto Route 8")
    L.shot("route8_seam")
    L.leaveEdge("right", S.MAP_CITY)
    expect(L.mapId() == S.MAP_CITY, "Route 8 crosses back through the Neistan Gate")
    L.leaveEdge("down", S.MAP_R7)
    expect(L.mapId() == S.MAP_R7, "the Elektran Gate crosses onto Route 7")
    L.shot("route7_seam")
    L.leaveEdge("up", S.MAP_CITY)
    expect(L.mapId() == S.MAP_CITY, "Route 7 crosses back through the Elektran Gate")
    L.shot("back_in_town")
end)
