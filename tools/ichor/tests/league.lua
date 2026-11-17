local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
S.SCRIPTS = dofile(L.OUT .. "league_symbols.lua")
for k, v in pairs(dofile(L.OUT .. "league_callbacks.lua")) do S[k] = v end

local function hof() return L.on("CB2_HallOfFame") or L.on("CB2_DoHallOfFameScreen") end
local function credits() return L.on("CB2_IchorCredits") or L.on("CB2_StartIchorCredits") end

local function arrive(map, what)
    L.waitUntil(function() return L.mapId() == map end, 1200, what)
    L.settle()
    L.expect(L.mapId() == map, what)
end

-- The assisted team's stats: the flow is under test here, not the balance, so the
-- level-100 lead's stats are raised past anything the League can answer (struct
-- Pokemon keeps HP, max HP and the five stats as plain u16s after the box data).
local function assist()
    local mon = L.partyMon(0)
    for i = 0, 6 do emu:write16(mon + S.OFF_MON_HP + i * 2, 999) end
end

-- The assist between seats: HP and PP back, as a level-100 sweeper with one
-- move would otherwise run its PP dry (the League itself never heals here).
local function heal()
    L.setVar(S.VAR_TEMP_0, 0)
    L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                     S.SCR_OP_CALLNATIVE, { S.HealPlayerParty | 1, 4 }, S.SCR_OP_END })
    L.waitUntil(function() return L.getVar(S.VAR_TEMP_0) == 1 end, 120, "the assist's heal")
    L.wait(4)
    assist()
end

local function beat(script, flag, what)
    heal()
    L.talk(L.npc(script))
    L.expect(L.getFlag(flag), what)
end

L.start(function()
    L.quickstart()
    L.runHeader("League_SetupHeader")
    assist()
    L.expect(L.mapId() == S.MAP_ASTYRA, "the setup reaches Astyra's east road")

    -- the placeholder road: Astyra's muleteer, gated on all eight Laurels
    L.talk(L.npc("Astyra_EventScript_Muleteer"), {answers = {"yes"}})
    arrive(S.MAP_ASCENT_1F, "the muleteer carries eight Laurels to the foot of the Ascent")
    L.runHeader("League_DayHeader")
    L.shot("ascent_1f_road_end")

    -- 1F: the coast road, the bends, the beacon knoll; up into the cloud
    L.leaveEdge("up", S.MAP_ASCENT_2F)
    arrive(S.MAP_ASCENT_2F, "the slopes' road climbs into the cloud ledges")
    L.shot("ascent_2f_landing")

    -- 2F: the camp's cook is the midway rest
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.talk(L.npc("Ascent_2F_EventScript_Cook"))
    L.expect(L.partyHp(0) > 1, "the ex-Titanborn cook heals the party at the camp")
    L.expect(L.getFlag(S.FLAG_LEFTOVERS) and L.itemCount(S.ITEM_LEFTOVERS) == 1, "the cook's Leftovers, once")
    L.talk(L.npc("Ascent_2F_EventScript_Cook"))
    L.expect(L.itemCount(S.ITEM_LEFTOVERS) == 1, "the Leftovers cannot be duplicated")
    L.shot("ascent_2f_camp")
    L.leaveEdge("up", S.MAP_ASCENT_3F)
    arrive(S.MAP_ASCENT_3F, "the ledges climb out of the cloud to the snowline")
    L.shot("ascent_3f_snowline")

    -- 3F: the processional stair to the propylaia
    L.useWarp(S.MAP_PROPYLAIA)
    arrive(S.MAP_PROPYLAIA, "the stair ends at the Pantheon's propylaia")
    L.shot("propylaia")
    L.talk(L.npc("Olympus_Propylaia_EventScript_Guard"))
    L.expect(L.getFlag(S.FLAG_ENTERED), "the Archon's guard checks the eight Laurels and stands aside")

    -- a deliberate loss to the first seat: the whiteout resets the Pantheon
    L.talk(L.sign("Olympus_Propylaia_EventScript_InnerDoor"), {answers = {"yes"}})
    arrive(S.MAP_ARES, "the inner door leads to Ares's seat")
    L.expect(L.getVar(S.VAR_E4) == 1, "the walk-in shuts Ares's way in behind the player")
    L.shot("seat_of_ares")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.talk(L.npc("Olympus_SeatOfAres_EventScript_Brasidas"))
    L.battleMode = nil
    L.expect(L.mapId() == S.MAP_PROPYLAIA and not L.getFlag(S.FLAG_BRASIDAS) and L.getVar(S.VAR_E4) == 0,
             "losing in the Pantheon returns the player to the hearth and resets the seats")

    -- the run: four seats in order, no healing but the test's assist
    L.talk(L.sign("Olympus_Propylaia_EventScript_InnerDoor"), {answers = {"yes"}})
    arrive(S.MAP_ARES, "back into Ares's seat")
    beat("Olympus_SeatOfAres_EventScript_Brasidas", S.FLAG_BRASIDAS, "Brasidas, the Polemarch, falls")
    L.shot("seat_of_ares_won")
    L.useWarp(S.MAP_POSEIDON)
    arrive(S.MAP_POSEIDON, "Ares's far door opens on Poseidon's sea-court")
    L.expect(L.getVar(S.VAR_E4) == 3, "the sea-court's way in shuts")
    L.shot("seat_of_poseidon")
    beat("Olympus_SeatOfPoseidon_EventScript_Themistokles", S.FLAG_THEMISTOKLES, "Themistokles, the Admiral, falls")
    L.goTrigger(L.triggers("Olympus_SeatOfPoseidon_EventScript_ExitGate"))
    arrive(S.MAP_ATHENA, "the sea-court's gate opens on Athena's library")
    L.shot("seat_of_athena")
    beat("Olympus_SeatOfAthena_EventScript_Hypatia", S.FLAG_HYPATIA, "Hypatia, the Philosopher, falls")
    L.goTrigger(L.triggers("Olympus_SeatOfAthena_EventScript_ExitGate"))
    arrive(S.MAP_HERA, "the library's gate opens on Hera's hall")
    L.shot("seat_of_hera")
    beat("Olympus_SeatOfHera_EventScript_Olympias", S.FLAG_OLYMPIAS, "Olympias, the Serpent Queen, falls")

    -- the summit: the Archon, the knot, the Hall of Heroes
    heal()
    L.useWarp(S.MAP_SUMMIT, true)
    L.waitUntil(function() return L.mapId() == S.MAP_SUMMIT end, 1200, "the summit")
    L.wait(60)
    L.shot("summit_arrival")
    L.settle({stop = hof, answers = {"yes", "yes", "yes", "yes", "yes", "yes", "yes", "yes"}})
    L.waitUntil(hof, 3000, "the Hall of Fame screen")
    L.expect(L.defeated(S.T_ARISTEIDES) and L.getFlag(S.FLAG_ARCHON), "Aristeides, the Archon, falls")
    L.expect(L.getFlag(S.FLAG_KNOT), "two pairs of hands untie Medon's Knot")
    L.expect(L.getFlag(S.FLAG_UNWOVEN_STAR), "the Star Chart fills its last patch: the Unwoven")
    L.expect(L.getFlag(S.FLAG_GAME_CLEAR) and L.getFlag(S.FLAG_HIDE_ARCHON), "the game is clear and the Archon goes home")
    L.wait(240)
    L.shot("hall_of_heroes_screen")
    local t0 = L.now()
    while not credits() and L.now() - t0 < 12000 do
        L.tap(K.A)
        L.wait(30)
    end
    L.expect(credits(), "the Hall of Fame hands over to the credits")
    L.wait(600)
    L.shot("credits")

    -- CONTINUE: the next Klotheia in Elaia
    emu:reset()
    L.continueSave()
    L.settle({answers = {"yes"}})
    L.expect(L.mapId() == S.MAP_ROOM and L.getFlag(S.FLAG_EPILOGUE), "CONTINUE wakes the Archon of Aethos at home for the epilogue")
    L.shot("epilogue_room")
end)
