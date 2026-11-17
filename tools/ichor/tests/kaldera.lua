local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
S.SCRIPTS = dofile(L.OUT .. "kaldera_symbols.lua")
local T = "Kaldera_TempleOfHephaestus_EventScript_"
local F = "Kaldera_TelchinesForge_EventScript_"
local captain = "TriremeDeck_EventScript_Nausikles"

local function door(map, name)
    L.useWarp(map)
    L.settle()
    L.expect(L.mapId() == map, "actual connected door: " .. name)
    L.shot(name)
end

local function park(name, localId, flag, x, y)
    L.go(x - 3, y)
    L.face(K.RIGHT)
    for i = 1, 12 do
        L.waitUntil(function()
            local ox, oy = L.objectAt(localId)
            return ox == x and oy == y
        end, 900, name .. "'s actual feet to reach its plate")
        L.tap(K.A)
        L.wait(10)
        L.settle()
        if L.getFlag(flag) then break end
        L.wait(11 + i * 7)
    end
    L.expect(L.getFlag(flag), "the actual moving servant parks through its dial: " .. name)
    L.wait(60)
    local ox, oy = L.objectAt(localId)
    L.expect(ox == x and oy == y, "the live servant remains on its plate: " .. name)
    L.shot("servant_" .. name)
end

local function fillKeyPocket()
    local pocket, saved = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS, {}
    local key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
    for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
        local slot = pocket + i * S.ITEM_SLOT_SIZE
        saved[i] = {emu:read16(slot), emu:read16(slot + 2) ~ key}
        emu:write16(slot, S.ITEM_CONCH)
        emu:write16(slot + 2, 1 ~ key)
    end
    return function()
        pocket = L.sb1() + S.OFF_SB1_BAG + S.OFF_BAG_KEY_ITEMS
        key = emu:read32(L.sb2() + S.OFF_SB2_ENCRYPTION_KEY) & 0xFFFF
        for i = 0, S.BAG_KEYITEMS_COUNT - 1 do
            emu:write16(pocket + i * S.ITEM_SLOT_SIZE, saved[i][1])
            emu:write16(pocket + i * S.ITEM_SLOT_SIZE + 2, saved[i][2] ~ key)
        end
    end
end

L.start(function()
    L.quickstart()
    L.runHeader("Kaldera_SetupHeader")
    L.assistLevel100()
    L.talk(L.npc("Astyra_Harbor_EventScript_Mariner"))
    L.expect(L.mapId() == S.MAP_HARBOR, "Kaldera's story sailing waits for the Akropolis aftermath")
    L.setFlag(S.FLAG_RAID, true)
    L.talk(L.npc("Astyra_Harbor_EventScript_Mariner"), {menuChoice = 4})
    L.expect(L.mapId() == S.MAP_HARBOR, "STAY leaves the player on the actual quay")
    L.talk(L.npc("Astyra_Harbor_EventScript_Mariner"), {menuChoice = 3})
    L.expect(L.mapId() == S.MAP_DECK and L.getVar(S.VAR_DEST) == 4,
             "the unlocked story voyage boards the real Euploia")
    L.runHeader("Kaldera_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.mapId() == S.MAP_DECK and L.getVar(S.VAR_DEST) == 4,
             "the selected destination survives save/reset/CONTINUE aboard ship")
    L.talk(L.npc(captain), {answers = {"no"}})
    L.expect(L.mapId() == S.MAP_DECK, "the captain can wait before making port")
    L.talk(L.npc(captain), {answers = {"yes"}})
    L.expect(L.mapId() == S.MAP_KALDERA and L.getFlag(S.FLAG_ARRIVED)
             and L.itemCount(S.ITEM_CONCH) == 0 and not L.getFlag(S.FLAG_CONCH),
             "the story trireme reaches Kaldera without requiring or granting Surf")
    L.shot("thera_harbor")
    door(S.MAP_CLINIC, "caldera_asclepeion")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.talk(L.npc("Kaldera_Asclepeion_EventScript_Healer"))
    L.expect(emu:read16(L.partyMon(0) + S.OFF_MON_HP) > 1, "the island's actual healer restores the party")
    door(S.MAP_KALDERA, "clinic_return")
    door(S.MAP_AGORA, "caldera_agora")
    door(S.MAP_KALDERA, "agora_return")
    door(S.MAP_HOUSE, "smiths_house")
    L.talk(L.npc("Kaldera_SmithsHouse_EventScript_Smith"))
    L.talk(L.npc("Kaldera_SmithsHouse_EventScript_Smith"))
    L.expect(L.getFlag(S.FLAG_GIFT) and L.itemCount(S.ITEM_COAT) == 1,
             "the smith's household has a real, nonduplicating gift")
    door(S.MAP_KALDERA, "smith_return")
    door(S.MAP_FORGE, "forge_before_laurel")
    L.expect(not L.canReachNextTo(21, 8), "the actual inner forge stays closed before the Forge Laurel")
    door(S.MAP_KALDERA, "forge_return")
    door(S.MAP_TEMPLE, "bronze_servants")
    L.expect(not L.canReachNextTo(14, 3), "the three real shutters block a first-time approach to Talos")
    L.talk(L.npc(T .. "SmithOne"))
    L.go(7, 39)
    L.face(K.RIGHT)
    L.waitUntil(function()
        local x, y = L.objectAt(S.LOCAL_TEACH)
        return x == 10 and y == 38
    end, 900, "the first servant to leave its plate")
    L.tap(K.A)
    L.wait(10)
    L.settle()
    L.expect(not L.getFlag(S.FLAG_TEACH) and not L.getFlag(S.TEMP_TEACH),
             "a genuinely mistimed dial cannot open the shutter")
    park("Teach", S.LOCAL_TEACH, S.TEMP_TEACH, 10, 39)
    L.expect(L.getFlag(S.FLAG_TEACH), "the taught single-servant plate opens its actual shutter")
    L.talk(L.npc(T .. "SmithTwo"))
    park("TestOne", S.LOCAL_TEST_ONE, S.TEMP_TEST_ONE, 9, 25)
    park("TestTwo", S.LOCAL_TEST_TWO, S.TEMP_TEST_TWO, 18, 25)
    L.expect(L.getFlag(S.FLAG_TEST), "two parked servants open the second actual shutter")
    door(S.MAP_KALDERA, "solved_rooms_return")
    door(S.MAP_TEMPLE, "solved_rooms_reentry")
    L.expect(L.getFlag(S.FLAG_TEACH) and L.getFlag(S.FLAG_TEST) and L.canReachNextTo(14, 10),
             "the first two solved shutters survive leaving and reentering")
    L.go(19, 13)
    L.talk(20, 13, {answers = {"yes"}})
    L.step(K.RIGHT)
    local wrongX, wrongY = L.objectAt(S.LOCAL_DRUM)
    L.expect(wrongX == 21 and wrongY == 13, "the drum can actually be pushed away from its solution")
    L.talk(L.sign(T .. "Rule"), {answers = {"yes"}})
    L.expect(L.getFlag(S.FLAG_TEACH) and L.getFlag(S.FLAG_TEST),
             "the real reset tablet preserves the saved solved shutters")
    park("MasterOne", S.LOCAL_MASTER_ONE, S.TEMP_MASTER_ONE, 8, 11)
    park("MasterTwo", S.LOCAL_MASTER_TWO, S.TEMP_MASTER_TWO, 14, 11)
    L.go(20, 14)
    L.talk(20, 13, {answers = {"yes"}})
    L.step(K.UP)
    L.settle()
    local dx, dy = L.objectAt(S.LOCAL_DRUM)
    L.expect(dx == 20 and dy == 12, "the actual Girdle pushes the actual drum into the last loop")
    L.go(17, 11)
    L.waitUntil(function()
        local x, y = L.objectAt(S.LOCAL_MASTER_THREE)
        return x == 20 and y == 11
    end, 900, "the drum to cut the third servant's real loop")
    L.wait(80)
    local sx, sy = L.objectAt(S.LOCAL_MASTER_THREE)
    L.expect(sx == 20 and sy == 11 and not L.getFlag(S.TEMP_MASTER_THREE),
             "the actual drum holds the moving servant on the plate before the dial is turned")
    park("MasterThree", S.LOCAL_MASTER_THREE, S.TEMP_MASTER_THREE, 20, 11)
    L.expect(L.getFlag(S.FLAG_MASTER) and L.canReachNextTo(14, 3),
             "three real servants and the positioned drum open the great anvil")
    L.shot("master_servants")
    L.talk(L.npc(T .. "SmithThree"))
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.talk(L.npc(T .. "Talos"))
    L.battleMode = nil
    L.expect(L.mapId() == S.MAP_CLINIC and not L.getFlag(S.FLAG_LAUREL),
             "losing to Talos recovers locally without granting the Laurel")
    door(S.MAP_KALDERA, "talos_retry_town")
    door(S.MAP_TEMPLE, "talos_retry")
    L.talk(L.npc(T .. "Talos"))
    L.expect(L.getFlag(S.FLAG_LAUREL) and L.mapId() == S.MAP_FORGE,
             "beating Talos earns Laurel 6 and leads into the Telchines forge")
    local restore = fillKeyPocket()
    L.talk(L.npc(F .. "Talos"))
    L.expect(not L.getFlag(S.FLAG_WINGS) and not L.getFlag(S.FLAG_SECRET),
             "a full pocket cannot advance the Wings handover")
    restore()
    L.talk(L.npc(F .. "Talos"))
    L.expect(L.getFlag(S.FLAG_WINGS) and L.getFlag(S.FLAG_SECRET) and L.itemCount(S.ITEM_WINGS) == 1,
             "Talos's actual handover grants the canonical Wings and the Harpe revelation")
    L.talk(L.npc(F .. "Talos"))
    L.expect(L.itemCount(S.ITEM_WINGS) == 1, "the Wings cannot be duplicated by talking again")
    L.talk(L.sign(F .. "Rest"))
    L.talk(L.npc(F .. "Petros"))
    L.talk(L.npc(F .. "Amathos"))
    L.talk(L.npc(F .. "Phlogios"))
    L.talk(L.sign(F .. "Rest"))
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.talk(L.npc(F .. "Hyperion"))
    L.battleMode = nil
    L.expect(L.mapId() == S.MAP_CLINIC and not L.getFlag(S.FLAG_FRAGMENT)
             and not L.getFlag(S.FLAG_MISSING) and L.getFlag(S.FLAG_WINGS),
             "an actual eruption whiteout preserves the Wings without stealing the fragment or sending the letter")
    door(S.MAP_KALDERA, "eruption_retry_town")
    door(S.MAP_FORGE, "eruption_retry")
    L.talk(L.npc(F .. "Hyperion"))
    L.expect(L.mapId() == S.MAP_KALDERA and L.getFlag(S.FLAG_FRAGMENT) and L.getFlag(S.FLAG_MISSING),
             "Hyperion's actual defeat leads to the third-fragment escape and Kydippe's harbor letter")
    L.shot("letter_from_home")
    L.runHeader("Kaldera_SaveHeader")
    L.runHeader("Kaldera_HomeHeader")
    L.expect(not L.npc("ElaiaVillage_PlayersHouse_1F_EventScript_Mom").present,
             "the letter actually removes Mom from the player's home")
    L.talk(L.sign("ElaiaVillage_PlayersHouse_1F_EventScript_HoneyShelf"))
    emu:reset()
    L.continueSave()
    L.expect(L.mapId() == S.MAP_KALDERA and L.getFlag(S.FLAG_LAUREL)
             and L.getFlag(S.FLAG_MASTER) and L.getFlag(S.FLAG_WINGS)
             and L.getFlag(S.FLAG_SECRET) and L.getFlag(S.FLAG_FRAGMENT)
             and L.getFlag(S.FLAG_MISSING) and L.itemCount(S.ITEM_WINGS) == 1,
             "the connected chapter survives an actual save/reset/CONTINUE")
    L.talk(L.npc("Kaldera_EventScript_Nausikles"), {menuChoice = 2})
    L.talk(L.npc(captain), {answers = {"yes"}})
    L.expect(L.mapId() == S.MAP_HARBOR, "the same trireme returns to the capital after the low point")
end)
