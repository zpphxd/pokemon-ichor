-- The Arkadia cluster ported from world-act2: doors both ways, the seams, the rooms' gifts.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S = L.S
for k, v in pairs(dofile(L.OUT .. "arkadia_town_symbols.lua")) do S.SCRIPTS[k] = v end
local expect = L.expect

-- Through the door to `map` and back: the return lands on the tile below the door.
local function door(home, homeName, map, name, inside)
    L.useWarp(map)
    expect(L.mapId() == map, "the " .. name .. " door opens")
    L.shot(name)
    if inside then inside() end
    L.useWarp(home)
    expect(L.mapId() == home, "the " .. name .. " returns to " .. homeName)
    local x, y = L.pos()
    local ok = false
    for _, w in ipairs(L.mapEvents().warps) do
        if w.map == map and w.x == x and w.y + 1 == y then ok = true end
    end
    expect(ok, string.format("the %s returns in front of its own door (%d,%d)", name, x, y))
end
local function cross(dir, map, name)
    L.leaveEdge(dir, map)
    expect(L.mapId() == map, "the seam crosses: " .. name)
    L.shot(name)
end

L.start(function()
    L.quickstart()
    L.runHeader("ArkadiaTown_SetupHeader")
    expect(L.mapId() == S.MAP_ARKADIA, "arrived before the Temple of Artemis")
    L.shot("temple_stair")
    local A = S.MAP_ARKADIA
    door(A, "Arkadia", S.MAP_TEMPLE, "temple")
    door(A, "Arkadia", S.MAP_CLINIC, "asclepeion")
    door(A, "Arkadia", S.MAP_AGORA, "agora")
    door(A, "Arkadia", S.MAP_CHARCOAL, "charcoal_hut", function()
        L.talk(L.npc("Arkadia_CharcoalHut_EventScript_Hippothoos"), {answers = {"no"}})
        expect(L.idle(), "Hippothoos's trade can be turned down")
    end)
    door(A, "Arkadia", S.MAP_NYKTIMOS, "nyktimos_hall", function()
        L.talk(L.npc("Arkadia_NyktimosHall_EventScript_Nyktimos"), {menuChoice = 4})
        expect(L.getFlag(S.FLAG_GLASSES) and L.itemCount(S.ITEM_BLACK_GLASSES) == 1,
               "Nyktimos gives the Black Glasses after the Moon Laurel")
        expect(L.idle(), "Nyktimos's rest offer returns control")
    end)
    for n, flag in ipairs({S.FLAG_KID_1, S.FLAG_KID_2, S.FLAG_KID_3}) do
        L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_LostKid" .. n))
        expect(L.getFlag(flag), "Krotos's lost kid " .. n .. " goes home")
    end
    door(A, "Arkadia", S.MAP_GOATHERD, "goatherd_house", function()
        L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_Krotos"))
        expect(L.getFlag(S.FLAG_LUCKY_EGG) and L.itemCount(S.ITEM_LUCKY_EGG) == 1,
               "Krotos gives the Lucky Egg for his three kids")
    end)
    door(A, "Arkadia", S.MAP_WOOD, "cypress_wood")
    -- Klymene's race: out of her door, the temple stair's first step, and back in.
    L.useWarp(S.MAP_KLYMENE)
    expect(L.mapId() == S.MAP_KLYMENE, "the klymene_house door opens")
    L.talk(L.npc("Arkadia_KlymeneHouse_EventScript_Klymene"), {answers = {"yes"}})
    expect(L.mapId() == A, "the race starts at Klymene's door")
    L.goTrigger(L.triggers("Arkadia_KlymeneHouse_EventScript_RaceTurn"))
    L.settle()
    L.useWarp(S.MAP_KLYMENE)
    L.settle()
    expect(L.getFlag(S.FLAG_SCARF) and L.itemCount(S.ITEM_CHOICE_SCARF) == 1,
           "the shortest race beats Parthenopaios for the Choice Scarf")
    L.shot("klymene_race")
    L.useWarp(A)
    expect(L.mapId() == A, "Klymene's house returns to Arkadia")
    cross("right", S.MAP_R13, "route13_seam")
    cross("left", A, "back_from_route13")
    cross("up", S.MAP_R12, "route12_seam")
    door(S.MAP_R12, "Route 12", S.MAP_CAVE, "cave_of_maia", function()
        L.talk(L.npc("Route12_CaveOfMaia_EventScript_Priestess"))
        expect(L.idle(), "the priestess's rest returns control")
    end)
    cross("up", S.MAP_STYX, "styx_seam")
    local Y = S.MAP_STYX
    door(Y, "Styx Falls", S.MAP_INN, "inn", function()
        L.talk(L.npc("StyxFalls_Inn_EventScript_Eubouleus"), {answers = {"yes"}})
        expect(L.getFlag(S.FLAG_GRYLLOS), "Eubouleus hands over Gryllos")
        L.talk(L.npc("StyxFalls_Inn_EventScript_Aroanios"), {menuChoice = 4})
        expect(L.idle(), "the inn's rest offer returns control")
    end)
    door(Y, "Styx Falls", S.MAP_OATH, "oath_house", function()
        L.talk(L.npc("StyxFalls_OathHouse_EventScript_Horkia"))
        expect(L.getFlag(S.FLAG_CLEANSE_TAG) and L.itemCount(S.ITEM_CLEANSE_TAG) == 1, "Horkia gives the Cleanse Tag")
    end)
    door(Y, "Styx Falls", S.MAP_STONE, "stone_house", function()
        L.talk(L.npc("StyxFalls_StoneHouse_EventScript_Kepheus"))
        expect(L.getFlag(S.FLAG_BULLDOZE) and L.itemCount(S.ITEM_TM_BULLDOZE) == 1, "Kepheus gives TM Bulldoze")
    end)
    cross("up", S.MAP_R11, "drum_pass_seam")
    cross("down", Y, "back_from_drum_pass")
    cross("down", S.MAP_R12, "back_from_styx")
    cross("down", A, "back_to_arkadia")
end)
