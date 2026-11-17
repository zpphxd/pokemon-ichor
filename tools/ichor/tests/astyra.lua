local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "astyra_symbols.lua")) do S.SCRIPTS[k] = v end
local function cross(dir, map, name)
    L.leaveEdge(dir, map)
    L.expect(L.mapId() == map, "actual connected crossing: " .. name)
    L.shot(name)
end
local function door(map, name, scene)
    L.useWarp(map, scene)
    if scene then L.settle() end
    L.expect(L.mapId() == map, "actual door: " .. name)
    L.shot(name)
end
local counts, votes, watchCount = {}, {}, false
local courtShots = {}
local multiCount = 0
local battle = L.battle
function L.battle()
    if L.mapId() == S.MAP_AKROPOLIS
       and emu:read32(S.gBattleTypeFlags) & S.MULTI_TYPES == S.MULTI_TYPES then
        multiCount = multiCount + 1
        L.expect(emu:read16(S.SCRIPTS.gPartnerTrainerId) == S.ALETHEA_PARTNER,
                 "the Akropolis battle uses actual Alethea as the AI partner against two trainers")
        if L.battleMode == "lose" then
            for i = 0, 1 do
                emu:write16(L.partyMon(i + S.B_TRAINER_PARTNER * 6) + S.OFF_MON_HP, 1)
            end
        end
    end
    return battle()
end
local logText = L.logText
function L.logText()
    logText()
    if L.mapId() == S.MAP_AKROPOLIS then
        local _, y = L.pos()
        local name = L.getFlag(S.FLAG_OLIVE) and "fallen_olive" or "olive_before_raid"
        if y <= 11 and not courtShots[name] then
            courtShots[name] = true
            L.shot(name)
        end
    end
    if not watchCount or L.mapId() ~= S.MAP_STOA then return end
    for i = 1, 6 do
        local voter = L.npc("Astyra_Stoa_EventScript_Citizen", i)
        if not votes[i] and voter.present and voter.x == 16 and voter.y == 16 then
            votes[i] = true
            L.shot("assembly_vote_" .. i)
        end
    end
    for _, name in ipairs({"CountFirst", "CountSecond", "CountFinal"}) do
        if not counts[name] then
            local addr, same = S.SCRIPTS["AstyraStoa_Text_" .. name], true
            for i = 0, 127 do
                local b = emu:read8(addr + i)
                if emu:read8(S.gStringVar4 + i) ~= b then same = false break end
                if b == 0xFF then break end
            end
            if same then
                counts[name] = true
                L.expect(emu:read8(S.gTimeOfDay) == S.TIME_DAY, "Assembly count is staged in actual daylight")
                L.shot("assembly_" .. name)
            end
        end
    end
end
local function leave()
    L.useWarp(S.MAP_ASTYRA)
end
local function herm(script, flag)
    local oil = L.itemCount(S.ITEM_OIL)
    L.talk(L.sign(script), {answers = {0}})
    L.expect(L.getFlag(flag) and L.itemCount(S.ITEM_OIL) == oil - 1,
             "anointing consumes actual oil: " .. script)
end
L.start(function()
    L.quickstart()
    L.runHeader("Astyra_EarlyHeader")
    L.setBeat("capital_road", false)
    L.go(47, 25)
    L.tap(K.RIGHT, 8)
    L.settle()
    local x = L.pos()
    L.expect(L.mapId() == S.MAP_ELEUSA and x == 47,
             "Eleusa's actual eastern seam cannot skip the Moon Laurel chapter")
    L.runHeader("Astyra_MoonHeader")
    cross("right", S.MAP_R15, "salt_lakes")
    herm("Route15_MysteryRoad_EventScript_Herm", S.FLAG_R15_HERM)
    local potions, honey = L.itemCount(S.ITEM_HYPER_POTION), L.itemCount(S.ITEM_HONEY)
    L.talk(L.ball(S.FLAG_R15_JAR))
    L.talk(L.hidden(S.FLAG_R15_HIDDEN))
    L.expect(L.getFlag(S.FLAG_R15_JAR) and L.itemCount(S.ITEM_HYPER_POTION) == potions + 1,
             "the salt-lake jar grants a real healing item")
    L.expect(L.getFlag(S.FLAG_R15_HIDDEN) and L.itemCount(S.ITEM_HONEY) == honey + 1,
             "the salt-lake hidden reward is persistent")
    cross("right", S.MAP_DAPHNI, "daphni")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.talk(L.npc("Daphni_EventScript_Healer"))
    L.expect(emu:read16(L.partyMon(0) + S.OFF_MON_HP) > 1, "Daphni actually heals the party")
    cross("right", S.MAP_R16, "capital_pass")
    herm("Route16_CapitalPass_EventScript_Herm", S.FLAG_R16_HERM)
    cross("right", S.MAP_ASTYRA, "astyra")
    L.talk(L.npc("Astyra_EventScript_Preacher"))
    L.talk(L.npc("Astyra_EventScript_Herald"))
    L.talk(L.sign("Astyra_EventScript_Kodros"))
    L.talk(L.sign("Astyra_EventScript_Kairos"))
    L.talk(L.sign("Astyra_EventScript_Perdix"))
    L.useWarp(S.MAP_AKROPOLIS, true)
    L.settle()
    L.expect(L.mapId() == S.MAP_ASTYRA and not L.getFlag(S.FLAG_GATE),
             "the real Akropolis entrance cannot bypass the exile and roadside confession")
    L.useWarp(S.MAP_STOA, true)
    L.settle()
    L.expect(L.mapId() == S.MAP_ASTYRA and not L.getFlag(S.FLAG_OSTRACISM),
             "the Assembly cannot skip the Phaedon, Elpis and Daphne story seeds")
    door(S.MAP_HOUSE, "elpis_before_doctor", true)
    L.talk(L.npc("Astyra_PhaedonsHouse_EventScript_Elpis"))
    L.expect(not L.getFlag(S.FLAG_VISIT)
             and not L.npc("Astyra_PhaedonsHouse_EventScript_Visitor", 1).present,
             "visiting Elpis first leaves the later bedside exchange available")
    leave()
    door(S.MAP_CLINIC, "phaedon_clinic")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.talk(L.npc("Astyra_Asclepeion_EventScript_Phaedon"))
    L.expect(L.getFlag(S.FLAG_PHAEDON) and emu:read16(L.partyMon(0) + S.OFF_MON_HP) > 1,
             "Phaedon is an actual repeatable healer, not only dialogue")
    L.talk(L.sign("Astyra_Asclepeion_EventScript_Hearth"))
    L.talk(L.npc("Astyra_Asclepeion_EventScript_Panacoil"))
    L.talk(L.sign("Astyra_Asclepeion_EventScript_Pithos"), {answers = {2}})
    L.expect(L.idle(), "the capital's actual Pithos menu opens and closes")
    leave()
    door(S.MAP_HOUSE, "elpis_room", true)
    L.expect(L.getFlag(S.FLAG_VISIT)
             and not L.npc("Astyra_PhaedonsHouse_EventScript_Visitor", 1).present
             and not L.npc("Astyra_PhaedonsHouse_EventScript_Visitor", 2).present,
             "Daphne and Phaedon's actual bedside exchange finishes and both visitors leave")
    L.expect(L.playing(S.MUS_LULLABY), "Elpis's room plays the composed lullaby")
    L.talk(L.npc("Astyra_PhaedonsHouse_EventScript_Elpis"))
    L.talk(L.sign("Astyra_PhaedonsHouse_EventScript_Starry"))
    L.talk(L.sign("Astyra_PhaedonsHouse_EventScript_MusicBox"))
    L.shot("elpis_and_starry")
    L.expect(L.getFlag(S.FLAG_ELPIS) and L.playing(S.MUS_LULLABY),
             "Elpis's receipt and the music-box return to her room's song work")
    leave()
    door(S.MAP_LIBRARY, "library")
    L.talk(L.npc("Astyra_Library_EventScript_Daphne"))
    L.talk(L.npc("Astyra_Library_EventScript_Librarian"), {answers = {0}})
    L.expect(not L.getFlag(S.FLAG_PAGE_V), "an incorrect Perdix answer cannot grant Page V")
    L.talk(L.npc("Astyra_Library_EventScript_Librarian"), {answers = {1}})
    L.expect(L.getFlag(S.FLAG_PAGE_V) and L.getFlag(S.FLAG_DAPHNE),
             "the plaque's actual answer grants canonical Page V after Daphne's scene")
    L.talk(L.npc("Astyra_Library_EventScript_Librarian"))
    L.shot("page_v")
    leave()
    watchCount = true
    L.useWarp(S.MAP_STOA, true)
    L.settle()
    watchCount = false
    local voteCount = 0
    for _ in pairs(votes) do voteCount = voteCount + 1 end
    L.expect(voteCount == 6, "all six distinct named citizens actually walk to the voting urn")
    L.expect(counts.CountFirst and counts.CountSecond and counts.CountFinal,
             "the actual count window shows 1,204, then 3,977, then 6,000+ and 389 others")
    L.expect(L.getFlag(S.FLAG_OSTRACISM) and L.mapId() == S.MAP_ASTYRA
             and not L.npc("Astyra_EventScript_Alethea").present,
             "the forged decree exiles Alethea and returns control to the real city")
    L.expect(L.playing(S.MUS_CITY), "decree silence does not stall the warp or leave city music paused")
    L.useWarp(S.MAP_STOA)
    L.talk(L.sign("Astyra_Stoa_EventScript_Count"))
    L.expect(L.idle() and not L.npc("Astyra_Stoa_EventScript_Alethea").present,
             "reentering the Assembly cannot replay the vote or restore the exile")
    L.shot("assembly_after_vote")
    leave()
    cross("left", S.MAP_R16, "road_back_to_daphni")
    L.expect(emu:read8(S.gTimeOfDay) == S.TIME_NIGHT,
             "the exile's roadside confession is available at staged night without a clock gate")
    L.talk(L.npc("Astyra_EventScript_RoadAlethea"))
    L.expect(L.getFlag(S.FLAG_CONFESSION) and not L.npc("Astyra_EventScript_RoadAlethea").present,
             "Alethea's actual reading and Keeper warning are saved before the raid")
    cross("right", S.MAP_ASTYRA, "return_for_raid")
    door(S.MAP_AKROPOLIS, "forged_order_gate", true)
    L.expect(L.getFlag(S.FLAG_GATE) and emu:read8(S.gTimeOfDay) == S.TIME_NIGHT,
             "the captain actually steps aside for the forged owl/hook order at staged night")
    L.go(17, 44)
    L.expect(emu:saveStateFile(L.OUT .. "before_multi_loss.ss", 31), "saved the partner loss branch")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.step(K.UP)
    L.settle()
    L.battleMode = nil
    L.expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST
             and L.mapId() == S.MAP_CLINIC and not L.getFlag(S.FLAG_PAIR_ONE),
             "a genuine multi loss retreats to Phaedon without granting the checkpoint")
    L.expect(emu:loadStateFile(L.OUT .. "before_multi_loss.ss", 31), "restored the partner climb")
    L.wait(30)
    L.waitUntil(L.idle, 600, "control after restoring the climb")
    L.go(17, 42)
    L.expect(L.getFlag(S.FLAG_PAIR_ONE), "Lithos and Koniortos must actually be defeated")
    L.talk(L.hidden(S.FLAG_RAID_REVIVE))
    L.go(17, 30)
    L.expect(L.getFlag(S.FLAG_PAIR_TWO) and multiCount == 3 and not L.getFlag(S.FLAG_RAID),
             "Sideros and Chalkos are a second distinct native multi battle, not a player double")
    local heals = L.itemCount(S.ITEM_HYPER_POTION)
    L.talk(L.npc("Astyra_Akropolis_EventScript_HealingJar"))
    L.expect(L.getFlag(S.FLAG_RAID_JAR) and L.itemCount(S.ITEM_HYPER_POTION) == heals + 1,
             "the Sacred Way's side branch pays with an actual healing supply")
    L.go(17, 18)
    L.expect(L.getFlag(S.FLAG_KLEON), "beating Kleon plays his they-want-you revelation")
    L.shot("parthenon_steps")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.goTrigger(L.triggers("Astyra_Akropolis_EventScript_Rhea"))
    L.settle()
    L.battleMode = nil
    L.expect(L.getFlag(S.FLAG_OLIVE) and not L.getFlag(S.FLAG_RAID) and L.mapId() == S.MAP_CLINIC,
             "a real Rhea whiteout keeps the uprooted olive but does not award raid completion")
    leave()
    L.useWarp(S.MAP_AKROPOLIS)
    L.goTrigger(L.triggers("Astyra_Akropolis_EventScript_Rhea"))
    L.settle()
    L.expect(L.getFlag(S.FLAG_OLIVE) and L.getFlag(S.FLAG_RAID) and L.mapId() == S.MAP_CLINIC,
             "Rhea's battle, escape with the second fragment and olive aftermath reach Phaedon")
    L.expect(L.getFlag(S.FLAG_RECOVERY) and emu:read8(L.ichor() + S.OFF_HELD_TIME) == 0,
             "Phaedon's actual recovery scene releases the staged night")
    L.shot("raid_recovery")
    leave()
    L.useWarp(S.MAP_AKROPOLIS)
    local fought = #L.battles
    L.go(17, 9)
    L.talk(L.npc("Astyra_Akropolis_EventScript_Caretaker"))
    L.expect(#L.battles == fought and L.grid().tile(16, 5) == 0x001
             and L.grid().tile(21, 6) == 0x0E1,
             "reentry preserves the fallen olive and collapsed spring without replaying combat")
    L.shot("olive_after_raid")
    L.talk(L.hidden(S.FLAG_RAID_ETHER))
    L.expect(L.getFlag(S.FLAG_RAID_REVIVE) and L.getFlag(S.FLAG_RAID_ETHER),
             "both curious terrace/court corners grant persistent hidden supplies")
    leave()
    cross("left", S.MAP_R16, "road_after_raid")
    L.expect(emu:saveStateFile(L.OUT .. "before_capital_loss.ss", 31), "saved the capital loss branch")
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.battleMode = "lose"
    L.talk(L.npc("Route16_CapitalPass_EventScript_EUBIOS"))
    L.battleMode = nil
    L.expect(L.battles[#L.battles].outcome == S.B_OUTCOME_LOST and L.mapId() == S.MAP_CLINIC,
             "an actual capital-road whiteout recovers with Phaedon")
    L.shot("phaedon_recovery")
    L.expect(emu:loadStateFile(L.OUT .. "before_capital_loss.ss", 31), "restored onward travel")
    L.wait(30)
    L.waitUntil(L.idle, 600, "control after restoring capital road")
    L.runHeader("Astyra_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.getFlag(S.FLAG_PAGE_V) and L.getFlag(S.FLAG_PHAEDON)
             and L.getFlag(S.FLAG_ELPIS) and L.getFlag(S.FLAG_DAPHNE)
             and L.getFlag(S.FLAG_VISIT) and L.getFlag(S.FLAG_OSTRACISM)
             and L.getFlag(S.FLAG_CONFESSION)
             and L.getFlag(S.FLAG_GATE) and L.getFlag(S.FLAG_PAIR_ONE)
             and L.getFlag(S.FLAG_PAIR_TWO) and L.getFlag(S.FLAG_KLEON)
             and L.getFlag(S.FLAG_OLIVE) and L.getFlag(S.FLAG_RAID)
             and L.getFlag(S.FLAG_RECOVERY)
             and L.getFlag(S.FLAG_RAID_JAR) and L.getFlag(S.FLAG_RAID_REVIVE)
             and L.getFlag(S.FLAG_RAID_ETHER)
             and L.getFlag(S.FLAG_R15_HERM) and L.getFlag(S.FLAG_R16_HERM),
             "capital scenes, canonical page and both herms survive save/reset/CONTINUE")
    cross("left", S.MAP_DAPHNI, "return_to_daphni")
    L.expect(emu:read8(L.ichor() + S.OFF_HELD_TIME) == 0,
             "leaving the staged chapter returns the world to its real clock")
    cross("left", S.MAP_R15, "return_to_salt_lakes")
    cross("left", S.MAP_ELEUSA, "return_to_eleusa")
end)
