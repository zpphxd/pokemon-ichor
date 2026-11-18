-- The Arkadia cluster ported from world-act2: doors both ways, the seams, the rooms' gifts.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K = L.S, L.K
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

local function gfxOf(localId)
    for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
        local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
        if L.emu:read8(o) & 1 == 1 and L.emu:read8(o + S.OFF_OBJ_LOCAL_ID) == localId then
            return L.emu:read16(o + S.OFF_OBJ_GRAPHICS_ID)
        end
    end
end
local function heldTime() return L.emu:read8(L.ichor() + S.OFF_HELD_TIME) end

-- Kleon's recruitment (STORY.md §7.2), a shot on every box: the cast in place,
-- Iapetos in his mask stepping out of the cypresses, a warm dusk at most, and
-- the clock's own light back afterwards.
local function recruitment()
    L.runHeader("ArkadiaTown_RecruitHeader")
    expect(L.mapId() == S.MAP_ARKADIA and not L.getFlag(S.FLAG_RECRUITED), "arrived before Kleon's choice")
    expect(heldTime() == 0, "Arkadia starts on the clock's own light")
    L.setBeat("kleons_choice", false)
    L.shot("before")
    local seen = {held = {}}
    L.goTrigger(L.triggers("Arkadia_EventScript_Recruitment"))
    L.settle({every = true, stop = function()
        local h = heldTime()
        seen.held[h] = true
        local ix, iy = L.objectAt(S.LOCALID_IAPETOS)
        if ix and not seen.iapetos then seen.iapetos = gfxOf(S.LOCALID_IAPETOS) end
        if ix and L.boxUp() then seen.iapetosAt = ix .. "," .. iy end
        if L.boxUp() and not seen.cast then
            local px, py = L.pos()
            local kx, ky = L.objectAt(S.LOCALID_KLEON)
            local ax, ay = L.objectAt(S.LOCALID_ALETHEA)
            seen.cast = string.format("%d,%d %d,%d %d,%d", px, py, kx or -1, ky or -1, ax or -1, ay or -1)
        end
        return false
    end})
    L.log("NOTE cast at the first box (player, Kleon, Alethea): " .. tostring(seen.cast))
    expect(seen.cast == "7,37 4,37 6,36", "the player stands three steps from Kleon with Alethea at the shoulder")
    expect(seen.iapetos == S.GFX_IAPETOS, "Iapetos wears his own mask, not a grunt's")
    expect(seen.iapetosAt == "2,37", "Iapetos steps out of the cypresses to face Kleon")
    expect(seen.held[S.TIME_EVENING + 1] and not seen.held[S.TIME_NIGHT + 1],
           "the scene holds a warm dusk, never full night")
    expect(heldTime() == 0, "the clock's own light returns after the scene")
    expect(L.getFlag(S.FLAG_RECRUITED) and L.getFlag(S.FLAG_HIDE_IAPETOS)
           and not L.objectAt(S.LOCALID_KLEON) and not L.objectAt(S.LOCALID_IAPETOS),
           "Kleon and Iapetos leave into the cypresses")
    L.shot("after")
    L.setBeat("boot", false)
end

L.start(function()
    L.quickstart()
    recruitment()
    L.runHeader("ArkadiaTown_SetupHeader")
    expect(L.mapId() == S.MAP_ARKADIA, "arrived before the Temple of Artemis")
    L.shot("temple_stair")
    -- the two huntresses gossip beside the cypress, not inside it (object_audit.py)
    L.go(22, 21)
    L.face(K.UP)
    L.shot("huntresses")
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
