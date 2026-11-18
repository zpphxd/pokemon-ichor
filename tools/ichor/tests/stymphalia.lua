-- The road north from Lakonia, walked (tools/ichor/maps/stymphalia.py): Route 26,
-- Lake Stymphalia and Route 27 into Arkadia, with a save and CONTINUE on the way.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "stymphalia_scripts.lua")) do S.SCRIPTS[k] = v end
local function flag(f, text) L.expect(L.getFlag(f), text) end
local function beaten(t, who) flag(S.TRAINER_FLAGS_START + t, who .. " is beaten") end

L.start(function()
    L.quickstart()
    L.runHeader("Stymphalia_SetupHeader")
    L.assistLevel100()
    L.settle()
    L.expect(L.mapId() == S.MAP_LAKONIA, "the test starts on Lakonia's north road")
    flag(S.FLAG_PARTED, "III-5J is done")
    L.shot("lakonia_north_open")

    -- Lakonia -> Route 26: the cadet has stepped out of the gap
    L.leaveEdge("up", S.MAP_ROUTE26)
    L.expect(L.mapId() == S.MAP_ROUTE26, "Lakonia's north road opens onto Route 26")
    L.shot("route26_south")
    L.go(15, 25)
    beaten(S.TRAINER_ANAXANDROS, "Anaxandros, on Herakles's bridge,")
    L.go(15, 15)
    L.shot("route26_fork")
    L.go(15, 4)
    beaten(S.TRAINER_DIENEKES, "Dienekes, in the Skiritis's gap,")
    L.leaveEdge("up", S.MAP_LAKE)
    L.expect(L.mapId() == S.MAP_LAKE, "Route 26's last rise comes down to Lake Stymphalia")

    -- the lake: the flock rises over the causeway; Akanthis's fire and herm
    L.go(21, 24)
    flag(S.FLAG_FLOCK, "the bronze flock rose the first time over the causeway")
    L.shot("lake_flock")
    L.talk(L.npc("LakeStymphalia_EventScript_Akanthis"))
    flag(S.FLAG_LERNIP_RUMOR, "Akanthis tells the deep reeds' rumor")
    flag(S.FLAG_TOWN_HERM, "Akanthis's fire registers the lake's travel herm")

    -- save on the causeway, reset, CONTINUE
    L.go(21, 25)
    L.runHeader("Stymphalia_SaveHeader")
    emu:reset()
    L.continueSave()
    L.expect(L.mapId() == S.MAP_LAKE, "CONTINUE puts the player back on Lake Stymphalia")
    L.expect(L.getFlag(S.FLAG_TOWN_HERM) and L.getFlag(S.FLAG_FLOCK), "the herm and the flock survive save/reset/CONTINUE")
    local x, y = L.pos()
    L.expect(x == 21 and y == 25, "CONTINUE resumes on the causeway where the game was saved")

    -- the long boardwalk and the islets, to the west shore
    L.go(21, 17)
    beaten(S.TRAINER_BORBOROS, "Borboros, on the long boardwalk,")
    L.go(4, 12)
    beaten(S.TRAINER_TENAGOS, "Tenagos, on the west boardwalk,")
    L.shot("lake_west_shore")
    L.leaveEdge("left", S.MAP_ROUTE27)
    L.expect(L.mapId() == S.MAP_ROUTE27, "the lake's west shore climbs onto Route 27")

    -- Route 27: the narrows, Othryades's bridge, the spring, the top of the pass
    L.runHeader("Stymphalia_HealHeader")
    L.go(21, 26)
    beaten(S.TRAINER_LOCHAGOS, "the scout at the narrows")
    L.runHeader("Stymphalia_HealHeader")
    L.go(21, 17)
    beaten(S.TRAINER_OTHRYADES, "Othryades, at the ravine bridge,")
    L.shot("route27_spring")
    L.runHeader("Stymphalia_HealHeader")
    L.go(7, 4)
    beaten(S.TRAINER_STHENELAIDAS, "Sthenelaidas, at the top of the pass,")
    L.leaveEdge("up", S.MAP_ARKADIA)
    L.expect(L.mapId() == S.MAP_ARKADIA, "Route 27 comes over the rise into Arkadia")
    L.shot("arkadia_from_the_south")
end)
