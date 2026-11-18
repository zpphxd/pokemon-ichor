local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
S.SCRIPTS = dofile(L.OUT .. "ascent_symbols.lua")
for k, v in pairs(dofile(L.OUT .. "ascent_callbacks.lua")) do S[k] = v end
local PLAN = dofile(L.OUT .. "ascent_plans.lua")
local OP = dofile(L.OUT .. "oros_plans.lua")
local KEY = { U = K.UP, D = K.DOWN, L = K.LEFT, R = K.RIGHT }
local DXY = { U = { 0, -1 }, D = { 0, 1 }, L = { -1, 0 }, R = { 1, 0 } }

local function arrive(map, what)
    L.waitUntil(function() return L.mapId() == map end, 1200, what)
    L.settle()
    L.expect(L.mapId() == map, what)
end

-- The flow is under test, not the balance (the Regice lead with Flash Cannon,
-- which no Calm Mind Chionyad walls the way it walls Ice Beam): the level-100 lead's stats are
-- raised past anything the Ascent can answer, and HP and PP come back between
-- legs (the climb's own healing is checked at the camp).
local function assist()
    local mon = L.partyMon(0)
    for i = 0, 6 do emu:write16(mon + S.OFF_MON_HP + i * 2, 999) end
end

local function heal()
    L.setVar(S.VAR_TEMP_0, 0)
    L.runRamScript({ S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
                     S.SCR_OP_CALLNATIVE, { S.HealPlayerParty | 1, 4 }, S.SCR_OP_END })
    L.waitUntil(function() return L.getVar(S.VAR_TEMP_0) == 1 end, 120, "the assist's heal")
    L.wait(4)
    assist()
end

-- A minimal battle pilot: fight with the first move, and when the lead faints
-- (the climb's trainers come many to a leg, and the assist's stats don't survive
-- a battle's end), send out the next sweeper still standing.
L.pilot = {
    training = false,
    beginBattle = function() end,
    afterBattle = function() end,
    observeEvolution = function() end,
    learnMove = function() L.tap(K.B); L.wait(10) end,
    chooseAction = function() return false end,
    chooseMove = function() L.tap(K.UP); L.tap(K.LEFT); L.tap(K.A) end,
    chooseReplacement = function()
        local slot = 1
        while slot < 5 and L.partyHp(slot) == 0 do slot = slot + 1 end
        for _ = 1, slot do L.tap(K.DOWN); L.wait(6) end
        L.tap(K.A); L.wait(20)
        L.tap(K.A); L.wait(30)
    end,
}

-- Walks never route across slick ice: the pathfinder doesn't know it slides.
local function keepOffIce()
    local g, off = L.grid(), {}
    for y = 0, g.h - 1 do
        for x = 0, g.w - 1 do
            local _, _, b = g.tile(x, y)
            if b == S.MB_ICE then off[x .. "," .. y] = true end
        end
    end
    L.keepOff[L.mapId()] = off
end

-- Play a slide answer: each key moves the player until something stops them.
local function slide(keys, gx, gy, what)
    for i = 1, #keys do
        local c = keys:sub(i, i)
        local x0, y0 = L.pos()
        emu:addKey(KEY[c])
        L.waitUntil(function() local x, y = L.pos(); return x ~= x0 or y ~= y0 end, 90,
                    what .. ": slide " .. i .. " (" .. c .. ") from " .. x0 .. "," .. y0)
        emu:clearKey(KEY[c])
        local still, lx, ly = 0, L.pos()
        local t0 = L.now()
        while still < 10 and L.now() - t0 < 600 do
            L.wait(1)
            local x, y = L.pos()
            if x == lx and y == ly and L.idle() then still = still + 1 else still = 0; lx, ly = x, y end
        end
    end
    local x, y = L.pos()
    L.expect(x == gx and y == gy, what .. string.format(" (at %d,%d)", x, y))
end

-- Play a seal's pushes: walk behind the drum and walk into it. The first push
-- asks for the Girdle; after that Strength stays on until the map changes.
local function push(list, what)
    for i, p in ipairs(list) do
        local sx, sy, c = p[1], p[2], p[3]
        L.go(sx, sy)
        if i == 1 then
            L.talk(sx + DXY[c][1], sy + DXY[c][2], { answers = { "yes" } })
        end
        L.face(KEY[c])
        if os.getenv("ASCENT_SHOTS") then L.shot(string.format("push_%d", i)) end
        local r = L.step(KEY[c])
        if r == "taken" then L.settle() end
        local x, y = L.pos()
        L.expect(x == sx + DXY[c][1] and y == sy + DXY[c][2],
                 string.format("%s: push %d (%s) from %d,%d moves the drum and the player (at %d,%d, step %s)",
                               what, i, c, sx, sy, x, y, tostring(r)))
    end
    L.settle()
end

-- A post-game gate before the credits: its sign reads, and nothing opens or moves.
local function gateShut(script, what)
    L.expect(not L.getFlag(S.FLAG_GAME_CLEAR), what .. ": the game isn't cleared yet")
    local map = L.mapId()
    L.talk(L.sign(script))
    L.settle()
    local x, y = L.pos()
    L.talk(L.sign(script))
    L.settle()
    local x2, y2 = L.pos()
    L.expect(L.mapId() == map and x == x2 and y == y2, what .. " stays shut before the credits")
end

-- The Bronze Hammer on each of the ridge's storm rubble, checking each one goes.
local function breakRubble(R)
    local ids = { S.LOCAL_RUBBLE0, S.LOCAL_RUBBLE1, S.LOCAL_RUBBLE2, S.LOCAL_RUBBLE3 }
    for i, r in ipairs(R.rubble) do
        L.go(22, r[2] + 2)
        L.settle()
        if L.objectAt(ids[i]) then
            L.talk(r[1], r[2], { answers = { "yes" } })
            L.settle()
            L.waitUntil(function() return L.objectAt(ids[i]) == nil end, 300, "the Hammer breaks the rubble at " .. r[1] .. "," .. r[2])
        else
            L.expect(false, "the rubble at " .. r[1] .. "," .. r[2] .. " is on the map to break")
        end
    end
end

-- 3F and the Propylaia, as a function so ASCENT_FROM=3f can start the walk here.
local function climbTop()
    -- 3F: out of the cloud; the stair pairs, the grand entrance's first sight (the camera
    -- climbs the facade), the gatekeeper, the watch-post, the post-game sockets shut
    L.goTrigger(L.triggers("Ascent_3F_EventScript_CloudBreak"))
    L.settle()
    L.expect(L.getFlag(S.FLAG_CLOUD), "breaking through the cloud line plays its scene")
    L.go(22, 57)
    L.shot("3f_above_the_cloud")
    heal()
    L.go(22, 51)
    L.settle()
    for _, t in ipairs({ { S.T_STHENELOS, "Sthenelos" }, { S.T_HIPPIAS, "Hippias" } }) do
        if not L.defeated(t[1]) then L.talk(L.npc("Ascent_3F_EventScript_" .. t[2])); L.settle() end
    end
    L.expect(L.defeated(S.T_STHENELOS) and L.defeated(S.T_HIPPIAS), "the first stair's pair: Sthenelos and Hippias")
    heal()
    L.go(25, 44)
    L.settle()
    heal()
    gateShut("Ascent_3F_EventScript_Sockets", "the four sockets")
    L.go(22, 38)
    L.settle()
    heal()
    L.goTrigger(L.triggers("Ascent_3F_EventScript_Pantheon"))
    L.waitUntil(function() return L.getFlag(S.FLAG_PANTHEON) end, 1800, "the facade's first sight")
    L.settle()
    L.expect(L.getFlag(S.FLAG_PANTHEON), "the first sight of the Propylaia runs the camera up its facade")
    for y = 33, 28, -1 do
        heal()
        L.go(21, y)
        L.settle()
    end
    heal()
    if not L.defeated(S.T_POLYDAMAS) then
        L.talk(L.npc("Ascent_3F_EventScript_Polydamas"))
        L.settle()
    end
    L.expect(L.defeated(S.T_POLYDAMAS), "the gatekeeper, Polydamas, is beaten")
    local kx, ky = L.objectAt(S.LOCAL_KEEPER)
    L.expect(kx == 20, string.format("the gatekeeper steps aside off the stair's axis (at %s,%s)", kx, ky))
    L.shot("3f_gatekeeper_aside")
    -- the watch-post: seen, the player is sent back; under the Helm, let by
    L.go(14, 30)
    L.step(K.LEFT)
    L.settle()
    local hx, hy = L.pos()
    L.expect(hx == 14 and hy == 30, string.format("the watchman sends a seen climber back (at %d,%d)", hx, hy))
    L.setFlag(S.FLAG_HELM_ON, true)
    L.go(12, 30)
    hx, hy = L.pos()
    L.expect(hx == 12 and hy == 30, "under the Helm of Darkness the watchman lets the climber by")
    L.shot("3f_watch_post")
    L.go(14, 30)
    L.setFlag(S.FLAG_HELM_ON, false)
    L.go(21, 18)
    L.shot("3f_the_twelve")
    L.go(21, 11)
    L.shot("3f_propylaia_doors")
    L.useWarp(S.MAP_PROPYLAIA)
    arrive(S.MAP_PROPYLAIA, "the processional way ends at the Propylaia's bronze doors")
    L.shot("propylaia_lobby")
    L.talk(L.npc("Olympus_Propylaia_EventScript_Guard"))
    L.expect(L.getFlag(S.FLAG_ENTERED), "the Archon's guard lets the climber into the Pantheon")
    L.shot("propylaia")
end

-- Boreas's ridge, as a function so ASCENT_FROM=ridge can start the walk here.
local function climbRidge()
    -- Boreas's ridge: Nephele, the spine's pair, the Bellows of Boreas (the Hammer's
    -- rubble, then two drums on two plates; a wrong push and the lever first)
    heal()
    L.go(22, 36)
    L.settle()
    if not L.defeated(S.T_NEPHELE) then L.talk(L.npc("Ascent_WindRidge_EventScript_Nephele")); L.settle() end
    heal()
    L.go(22, 30)
    L.settle()
    for _, t in ipairs({ { S.T_OREITHYIA, "Oreithyia" }, { S.T_KALAIS, "Kalais" } }) do
        if not L.defeated(t[1]) then L.talk(L.npc("Ascent_WindRidge_EventScript_" .. t[2])); L.settle() end
    end
    L.expect(L.defeated(S.T_OREITHYIA) and L.defeated(S.T_KALAIS), "the spine's pair: Oreithyia and Kalais")
    heal()
    gateShut("Ascent_WindRidge_EventScript_CloudBridge", "the cloud bridge")
    local R = OP.windridge
    breakRubble(R)
    L.expect(not L.getFlag(S.FLAG_BAR), "the bar is down before the drums move")
    -- one push, then the lever sets both drums (and the rubble) back
    L.go(R.pushes[1][1], R.pushes[1][2])
    L.talk(R.drums[1][1], R.drums[1][2], { answers = { "yes" } })
    L.face(K.RIGHT)
    L.step(K.RIGHT)
    L.talk(L.sign("Ascent_WindRidge_EventScript_Lever"), { answers = { "yes" } })
    L.settle()
    local rx, ry = L.objectAt(S.LOCAL_RIDGE_DRUM0)
    L.expect(rx == R.drums[1][1] and ry == R.drums[1][2] and not L.getFlag(S.FLAG_BAR), "the ridge's lever sets the drums back")
    for _, id in ipairs({ S.LOCAL_RUBBLE0, S.LOCAL_RUBBLE1, S.LOCAL_RUBBLE2, S.LOCAL_RUBBLE3 }) do
        L.expect(L.objectAt(id) == nil, "the reset leaves the broken rubble broken")
    end
    local d1x, d1y = L.objectAt(S.LOCAL_RIDGE_DRUM1)
    L.expect(d1x == R.drums[2][1] and d1y == R.drums[2][2],
             string.format("the second drum is back on its spot (at %s,%s)", tostring(d1x), tostring(d1y)))
    push(R.pushes, "the Bellows of Boreas")
    L.expect(L.getFlag(S.FLAG_BAR), "two drums on two plates lift the bar off the last stair")
    L.shot("ridge_bar_up")
    heal()
end

L.start(function()
    L.quickstart()
    L.runHeader("Ascent_SetupHeader")
    assist()
    L.expect(L.mapId() == S.MAP_ASTYRA, "the setup reaches Astyra's east road")
    if os.getenv("ASCENT_FROM") == "3f" then
        L.runHeader("Ascent_TopHeader")
        arrive(S.MAP_ASCENT_3F, "the quick start reaches 3F")
        L.runHeader("Ascent_DayHeader")
        climbTop()
        return
    end
    if os.getenv("ASCENT_FROM") == "ridge" then
        L.runHeader("Ascent_RidgeHeader")
        arrive(S.MAP_RIDGE, "the quick start reaches Boreas's ridge")
        L.runHeader("Ascent_DayHeader")
        climbRidge()
        return
    end
    L.talk(L.npc("Astyra_EventScript_Muleteer"), { answers = { "yes" } })
    arrive(S.MAP_ASCENT_1F, "the muleteer carries eight Laurels to the foot of the Ascent")
    L.runHeader("Ascent_DayHeader")

    -- 1F: the coast road's pair, the bends, up into the cloud
    heal()
    L.leaveEdge("up", S.MAP_ASCENT_2F)
    arrive(S.MAP_ASCENT_2F, "the slopes climb into the cloud ledges")
    heal()
    L.shot("2f_landing")

    -- 2F: the ledge pair, the camp (the climb's one midway heal, and its herm)
    emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
    L.talk(L.npc("Ascent_2F_EventScript_Cook"))
    L.expect(L.partyHp(0) > 1, "the camp's cook heals the party: the climb's midway rest")
    L.expect(L.getFlag(S.FLAG_HERM_ASCENT), "the camp's rest registers the Ascent's travel herm")
    L.expect(L.getFlag(S.FLAG_LEFTOVERS), "the cook's Leftovers")
    L.shot("2f_camp")
    L.useWarp(S.MAP_SNOWFIELD)
    arrive(S.MAP_SNOWFIELD, "the top of the ledges comes out on the Leuke snowfield")
    L.shot("snowfield_arrival")

    -- the snowfield: post-game gates stay shut, the stair's pair, the Mirror Tarn (the warm-up)
    heal()
    gateShut("Ascent_Snowfield_EventScript_RopedCave", "the roped cave")
    gateShut("Ascent_Snowfield_EventScript_BronzeDoor", "the bronze door of the Twelve")
    keepOffIce()
    L.go(25, 33)
    L.settle()
    if not L.defeated(S.T_LEUKIPPOS) then L.talk(L.npc("Ascent_Snowfield_EventScript_Leukippos")); L.settle() end
    if not L.defeated(S.T_THEONOE) then L.talk(L.npc("Ascent_Snowfield_EventScript_Theonoe")); L.settle() end
    L.expect(L.defeated(S.T_LEUKIPPOS) and L.defeated(S.T_THEONOE), "the stair's pair: Leukippos and Theonoe")
    heal()
    L.go(OP.snowfield.shore[1], OP.snowfield.shore[2])
    slide(OP.snowfield.tarn, OP.snowfield.landing[1], OP.snowfield.landing[2], "the Mirror Tarn carries the player to the Icefall's mouth")
    L.shot("snowfield_mouth")
    L.useWarp(S.MAP_ICEFALL)
    arrive(S.MAP_ICEFALL, "the snowfield's cliff mouth goes into the Icefall")
    L.shot("icefall_entry")

    -- the Icefall: the slide hall, the gut's pair, the drum seal
    heal()
    keepOffIce()
    L.go(21, 34)
    slide(PLAN.icefall.gut, 21, 22, "the Icefall's slide hall carries the player to the gut")
    L.shot("icefall_gut")
    L.go(21, 15)
    L.settle()
    L.expect(L.defeated(S.T_CHIONE) and L.defeated(S.T_ARKTOS), "the gut's pair: Chione and Arktos both fight")
    L.expect(not L.getFlag(S.FLAG_GRATE), "the grate is down before the drum moves")
    push(PLAN.icefall.pushes, "the Icefall's seal")
    L.expect(L.getFlag(S.FLAG_GRATE), "one drum on one plate raises the Icefall's grate")
    L.shot("icefall_grate_open")
    heal()
    L.useWarp(S.MAP_GLACIER)
    arrive(S.MAP_GLACIER, "the Icefall's mouth opens on the Glacier, under open sky")
    L.shot("glacier_foot")

    -- the Glacier: the narrows' pair, the frozen lake (the main ice puzzle: a dead end
    -- and its reset first), the Gate of the Winds (a wrong push and the lever first)
    heal()
    keepOffIce()
    L.go(12, 53)
    L.settle()
    if not L.defeated(S.T_NIPHON) then L.talk(L.npc("Ascent_Glacier_EventScript_Niphon")); L.settle() end
    if not L.defeated(S.T_PHOLOE) then L.talk(L.npc("Ascent_Glacier_EventScript_Pholoe")); L.settle() end
    L.expect(L.defeated(S.T_NIPHON) and L.defeated(S.T_PHOLOE), "the narrows' pair: Niphon and Pholoe both fight")
    heal()
    local G = OP.glacier
    L.go(G.entry[1], G.entry[2])
    slide(G.dead, G.dead_at[1], G.dead_at[2], "a tempting line across the lake ends in a dead end")
    L.shot("glacier_dead_end")
    slide(G.back, G.entry[1], G.entry[2], "the dead end's only way on is back to the shore (the reset)")
    slide(G.up, 21, 33, "the frozen lake's answer reaches the stair to the court")
    L.shot("glacier_lake_solved")
    L.go(22, 29)
    L.shot("glacier_court")
    L.go(20, 27)
    L.talk(21, 27, { answers = { "yes" } })
    L.step(K.RIGHT)
    local wx, wy = L.objectAt(S.LOCAL_DRUM1)
    L.expect(wx == 22 and wy == 27, "the drum can really be pushed off its answer")
    L.talk(L.sign("Ascent_Glacier_EventScript_Lever"), { answers = { "yes" } })
    L.settle()
    wx, wy = L.objectAt(S.LOCAL_DRUM1)
    L.expect(wx == 21 and wy == 27 and not L.getFlag(S.FLAG_GATE), "the reset lever sets the drums back")
    push(G.pushes, "the Gate of the Winds")
    L.expect(L.getFlag(S.FLAG_GATE), "three drums on three plates open the Gate of the Winds")
    L.shot("glacier_gate_open")
    heal()

    -- the upper glacier: the Wings' updraft to the eyrie and back, Ariadne's Thread
    -- down the crevasse to the Vault's crack ledge and back, the post-game gates shut
    L.talk(L.sign("Ascent_Glacier_EventScript_Updraft"), { answers = { "yes" } })
    L.settle()
    local ex, ey = L.pos()
    L.expect(ex == 2 and ey == 11, string.format("Daedalus's Wings ride the updraft to the eyrie (at %d,%d)", ex, ey))
    L.shot("glacier_eyrie")
    L.talk(L.sign("Ascent_Glacier_EventScript_UpdraftBack"), { answers = { "yes" } })
    L.settle()
    ex, ey = L.pos()
    L.expect(ex == 9 and ey == 11, string.format("the updraft carries the player back across (at %d,%d)", ex, ey))
    gateShut("Ascent_Glacier_EventScript_StormFace", "the storm face")
    gateShut("Ascent_Glacier_EventScript_Couloir", "the couloir's great boulder")
    gateShut("Ascent_Glacier_EventScript_FrozenFall", "the frozen fall")
    L.talk(L.sign("Ascent_Glacier_EventScript_Crevasse"), { answers = { "yes" } })
    arrive(S.MAP_VAULT, "Ariadne's Thread lowers the player down the crevasse into the Crystal Vault")
    ex, ey = L.pos()
    L.expect(ex == 4 and ey == 2, string.format("the Thread lands on the crack's ledge (at %d,%d)", ex, ey))
    L.shot("vault_crack_ledge")
    L.talk(3, 1, { answers = { "yes" } })
    arrive(S.MAP_GLACIER, "the Thread climbs back up to the Glacier")
    keepOffIce()
    L.leaveEdge("up", S.MAP_RIDGE, true)
    L.waitUntil(function() return L.mapId() == S.MAP_RIDGE end, 600, "onto Boreas's ridge")
    L.settle()
    L.shot("ridge_foot")

    climbRidge()
    L.leaveEdge("up", S.MAP_ASCENT_3F, true)
    L.waitUntil(function() return L.mapId() == S.MAP_ASCENT_3F end, 600, "above the cloud")
    L.settle()

    climbTop()
end)
