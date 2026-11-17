-- Kythera ported from world-act3: the voyage, doors both ways, the land seams,
-- the rooms' gifts and the Foam Laurel. Run by tools/ichor/tests/kythera_town.sh.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S = L.S
for k, v in pairs(dofile(L.OUT .. "kythera_town_symbols.lua")) do S.SCRIPTS[k] = v end
local expect = L.expect
local emu = L.emu

-- A minimal battle pilot for the two-partner assisted team: the first move
-- every turn, and the living partner in when one faints (L.battle's own loop
-- only knows a one-Pokémon party). Theion's Cairnolith can blow itself up.
L.pilot = {
    training = false,
    beginBattle = function() end,
    chooseAction = function() return false end,
    chooseMove = function() L.tap(L.K.UP); L.tap(L.K.LEFT); L.tap(L.K.A) end,
    observeEvolution = function() end,
    learnMove = function() L.tap(L.K.B); L.wait(20); L.tap(L.K.A) end,
    chooseReplacement = function()
        L.wait(30)
        L.tap(L.K.DOWN); L.wait(4)
        L.tap(L.K.A); L.wait(20); L.tap(L.K.A)
        L.waitUntil(L.inBattle, 1200, "the partner entering the battle")
        L.wait(30)
    end,
    -- the assisted team comes out of every fight rested: the check walks the
    -- maps, it doesn't grade Kythera's trainers (BALANCE.md's natural pilot does)
    afterBattle = function()
        for slot = 0, 1 do
            local mon = L.partyMon(slot)
            emu:write32(mon + S.OFF_MON_STATUS_K, 0)
            emu:write16(mon + S.OFF_MON_HP_K, emu:read16(mon + S.OFF_MON_MAXHP_K))
        end
    end,
}

-- Through the door to `map` and back: the return lands on the tile below the door.
local function door(home, homeName, map, name, inside)
    L.useWarp(map)
    L.settle()
    expect(L.mapId() == map, "the " .. name .. " door opens")
    L.shot(name)
    if inside then inside() end
    L.useWarp(home)
    L.settle()
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
    L.settle()
    expect(L.mapId() == map, "the seam crosses: " .. name)
    L.shot(name)
end
local function heal() L.runHeader("KytheraTown_HealHeader") end
local function gift(script, flag, item, what, opts)
    L.talk(L.npc(script), opts or { answers = { "yes", "yes" } })
    expect(L.getFlag(flag) and (item == nil or L.itemCount(item) == 1), what)
end

L.start(function()
    L.quickstart()
    L.runHeader("KytheraTown_SetupHeader")
    L.settle()
    expect(L.mapId() == S.MAP_KALDERA, "on Kaldera's quay after the letter")

    -- ---- the voyage: Kaldera, the southern deck, Melos ---------------------------------
    L.talk(L.npc("Kaldera_EventScript_Nausikles"), { menuChoice = 3, answers = { "yes" } })
    expect(L.mapId() == S.MAP_DECK_SOUTH and L.getVar(S.VAR_ACT3) == 1 and L.getFlag(S.FLAG_DAPHNE_SAILED),
           "Nausikles takes the player aboard; Daphne says goodbye and sails for Astyra")
    L.shot("deck_south_night")
    L.talk(L.npc("TriremeEuploia_DeckSouth_EventScript_Nausikles"), { answers = { "yes" } })
    expect(L.mapId() == S.MAP_MELOS and L.getFlag(S.FLAG_REACHED_MELOS), "the night crossing lands at Melos")
    L.shot("melos_jetty")

    local M = S.MAP_MELOS
    door(M, "Melos", S.MAP_FARMHOUSE, "farmhouse")
    L.talk(L.sign("Melos_EventScript_Seam"))
    expect(L.getFlag(S.FLAG_LUMP), "the slope's seam gives the lump of black glass")
    door(M, "Melos", S.MAP_KNAPPER, "knappers_house", function()
        gift("Melos_KnappersHouse_EventScript_Melanippos", S.FLAG_RAZOR_CLAW, S.ITEM_RAZOR_CLAW,
             "Melanippos knaps the lump into a Razor Claw")
    end)
    door(M, "Melos", S.MAP_BOATHOUSE, "boathouse", function()
        L.useWarp(S.MAP_LOFT)
        L.settle()
        expect(L.mapId() == S.MAP_LOFT, "the boathouse's ladder climbs to the loft")
        gift("Melos_BoathouseLoft_EventScript_Kalchedon", S.FLAG_DAMP_ROCK, S.ITEM_DAMP_ROCK,
             "Kalchedon gives the Damp Rock")
        L.useWarp(S.MAP_BOATHOUSE)
        L.settle()
        expect(L.mapId() == S.MAP_BOATHOUSE, "the loft's ladder comes back down")
    end)
    L.talk(L.npc("Melos_EventScript_Nausikles"), { answers = { "yes" } })
    expect(L.mapId() == S.MAP_SKANDEIA and L.getFlag(S.FLAG_CROSSED_ROUTE22), "the Euploia rounds Malea to Skandeia")
    expect(L.getFlag(S.FLAG_EUPLOIA_KEPT) and L.defeated(S.TRAINER_MOLYBDOS) and L.getVar(S.VAR_ACT3) == 2,
           "Molybdos's requisition is beaten off and the Euploia kept")
    L.shot("skandeia_quay")

    -- ---- Skandeia ------------------------------------------------------------------------
    local K = S.MAP_SKANDEIA
    door(K, "Skandeia", S.MAP_SK_CLINIC, "skandeia_asclepeion")
    door(K, "Skandeia", S.MAP_SK_AGORA, "skandeia_agora")
    L.goTrigger(L.triggers("KytheraSkandeia_EventScript_AletheaRejoins"))
    L.settle()
    expect(L.getFlag(S.FLAG_ALETHEA_REJOINED), "Alethea meets the player at the street's head")
    heal()
    door(K, "Skandeia", S.MAP_AXYLOS, "axylos_house", function()
        L.settle({ answers = { "yes", "yes", "yes" } })
        if not L.getFlag(S.FLAG_BAD_GUESTS_GONE) then
            L.talk(L.npc("KytheraSkandeia_AxylosHouse_EventScript_Axylos"), { answers = { "yes", "yes" } })
        end
        expect(L.getFlag(S.FLAG_BAD_GUESTS_GONE), "the bad guests are driven from Axylos's table")
    end)
    door(K, "Skandeia", S.MAP_NIKARETE, "nikarete_house")
    door(K, "Skandeia", S.MAP_PERFUMER, "perfumers_house", function()
        gift("KytheraSkandeia_PerfumersHouse_EventScript_Euodia", S.FLAG_SOOTHE_BELL, S.ITEM_SOOTHE_BELL,
             "Euodia gives the Soothe Bell")
    end)
    door(K, "Skandeia", S.MAP_DIVERS, "divers_house")
    door(K, "Skandeia", S.MAP_SHIPWRIGHT, "shipwrights_house")

    -- ---- the Foam Road, the spring and Echo's caves -----------------------------------------
    heal()
    cross("left", S.MAP_FOAM_ROAD, "foam_road_from_skandeia")
    cross("right", K, "skandeia_from_foam_road")
    cross("left", S.MAP_FOAM_ROAD, "foam_road_again")
    cross("up", S.MAP_SPRING, "spring_from_foam_road")
    door(S.MAP_SPRING, "the spring", S.MAP_CAVES, "echo_caves")
    cross("down", S.MAP_FOAM_ROAD, "foam_road_from_spring")
    heal()
    cross("left", S.MAP_PAPHIA, "paphia_from_foam_road")
    cross("right", S.MAP_FOAM_ROAD, "foam_road_from_paphia")
    cross("left", S.MAP_PAPHIA, "paphia_again")

    -- ---- Paphia ---------------------------------------------------------------------------
    heal()
    local P = S.MAP_PAPHIA
    door(P, "Paphia", S.MAP_PA_CLINIC, "paphia_asclepeion")
    door(P, "Paphia", S.MAP_PA_AGORA, "paphia_agora")
    door(P, "Paphia", S.MAP_PYGMALION, "pygmalions_workshop")
    door(P, "Paphia", S.MAP_DOVECOTE, "dovecote", function()
        L.talk(L.npc("KytheraPaphia_Dovecote_EventScript_Peristera"), { answers = { "yes" } })
        expect(L.getFlag(S.FLAG_EROSIE_EGG), "Peristera gives the Erosie egg")
    end)
    door(P, "Paphia", S.MAP_ORCHARD, "orchard_house")
    door(P, "Paphia", S.MAP_POTTER, "potters_house")

    -- ---- the Temple of Aphrodite: the Foam Laurel --------------------------------------------
    -- (two partners on the first move each turn can still be sung asleep and
    -- lose; a loss whites out to Paphia's Asclepeion, and the challenger walks
    -- back up the stair and tries again, as a player would)
    for attempt = 1, 3 do
        if L.mapId() == S.MAP_PA_CLINIC then
            L.useWarp(P)
            L.settle()
        end
        L.useWarp(S.MAP_TEMPLE)
        L.settle()
        expect(L.mapId() == S.MAP_TEMPLE, "the temple door opens")
        if attempt == 1 then L.shot("temple_pronaos") end
        L.runHeader("KytheraTown_FreezeHeader")
        heal()
        L.settle()
        L.talk(L.npc("KytheraTempleOfAphrodite_EventScript_Galatea"), { answers = { "yes", "yes" } })
        if L.getFlag(S.FLAG_BADGE07) then break end
        L.note("Galatea won attempt " .. attempt)
    end
    expect(L.defeated(S.TRAINER_GALATEA) and L.getFlag(S.FLAG_BADGE07) and L.getVar(S.VAR_ACT3) == 3,
           "Galatea gives the Foam Laurel")
    L.shot("foam_laurel")
    L.useWarp(P)
    L.settle()
    expect(L.mapId() == P, "the temple returns to Paphia")
    door(P, "Paphia", S.MAP_MIRROR, "mirror_house", function()
        gift("KytheraPaphia_MirrorHouse_EventScript_Leukippe", S.FLAG_MIRROR_HERB, S.ITEM_MIRROR_HERB,
             "Leukippe gives the Mirror Herb after the Foam Laurel")
    end)

    -- ---- the Neraida falls -----------------------------------------------------------------
    heal()
    cross("up", S.MAP_FALLS, "falls_from_paphia")
    door(S.MAP_FALLS, "the falls", S.MAP_MILL, "mill", function()
        gift("KytheraNeraidaFalls_Mill_EventScript_Myles", S.FLAG_METRONOME, S.ITEM_METRONOME,
             "Myles gives the Metronome")
    end)
    cross("down", P, "paphia_from_falls")
end)
