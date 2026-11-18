-- Pan's Crook: "Noon in Arkadia", then a face climbed up and down on two maps.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local extra = dofile(L.OUT .. "crook_symbols.lua")
for k, v in pairs(extra) do S.SCRIPTS[k] = v end
local expect = L.expect

local function at(x, y) local px, py = L.pos() return px == x and py == y end

-- Stand on (fx, fy), face `key`, press A and play out the climb (YES to the prompt).
local function climb(fx, fy, key, tx, ty, what)
    L.go(fx, fy)
    L.face(key)
    L.tap(K.A); L.wait(10)
    L.settle()
    local x, y = L.pos()
    expect(at(tx, ty), string.format("%s: lands on (%d,%d), at (%d,%d)", what, tx, ty, x, y))
    expect(L.idle(), what .. ": control comes back")
end

L.start(function()
    L.quickstart()
    L.runHeader("CrookClimb_SetupHeader")
    expect(L.mapId() == S.MAP_ARKADIA, "arrived in Arkadia after Laurel 5")
    local A = S.MAP_ARKADIA

    -- kid 3 sleeps in the grotto's mouth, the way to the crag: send it home first
    L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_LostKid3"))
    expect(L.getFlag(S.FLAG_KID_3), "the kid in the grotto mouth goes home")
    -- without the Crook the face only describes itself
    L.go(9, 13)
    L.face(K.UP)
    L.tap(K.A); L.wait(10)
    L.settle()
    expect(at(9, 13) and not L.getFlag(S.FLAG_GOT_CROOK), "no Crook: the handholds don't climb")
    L.shot("crag_before")

    -- Krotos tells of the kid on the crag
    L.useWarp(S.MAP_GOATHERD)
    L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_Krotos"))
    expect(L.getFlag(S.FLAG_HEARD), "Krotos tells of the kid on the crag over Pan's grotto")
    L.useWarp(A)

    -- the reeds by the falls pool, cut with the Sickle
    L.talk(L.npc("Arkadia_EventScript_LadonReeds"))
    expect(L.getFlag(S.FLAG_REEDS), "the Sickle cuts fresh reeds by the falls pool")

    -- pipe Pan awake
    L.talk(L.sign("Arkadia_EventScript_PansGrotto"))
    expect(L.getFlag(S.FLAG_WOKEN), "piping at the grotto wakes Pan (after the boar)")
    expect(L.getFlag(S.FLAG_GOT_CROOK) and L.itemCount(S.ITEM_PANS_CROOK) == 1, "Pan gives Pan's Crook")
    L.shot("got_crook")

    -- climb Arkadia's crag up, fetch the kid, climb back down
    climb(9, 13, K.UP, 9, 9, "Arkadia's crag, up")
    L.shot("crag_top")
    L.talk(L.npc("Arkadia_EventScript_CragKid"))
    expect(L.getFlag(S.FLAG_KID), "the kid is fetched down off the crag")
    climb(9, 9, K.DOWN, 9, 13, "Arkadia's crag, down")
    L.shot("crag_bottom")

    -- Krotos's thanks: a Kerazap
    L.useWarp(S.MAP_GOATHERD)
    L.talk(L.npc("Arkadia_GoatherdHouse_EventScript_Krotos"))
    expect(L.getFlag(S.FLAG_KERAZAP) and L.partyLevel(1) == 34, "Krotos gives the Kerazap, Lv 34")
    L.useWarp(A)

    -- Route 13: the scarp's face up to the crag pocket's PP Up, and back down
    L.leaveEdge("right", S.MAP_R13)
    expect(L.mapId() == S.MAP_R13, "on to Route 13")
    L.runHeader("CrookClimb_Route13Header")
    expect(L.mapId() == S.MAP_R13, "down on Route 13's valley road")
    climb(47, 17, K.UP, 47, 13, "Route 13's scarp, up")
    L.shot("r13_pocket")
    L.talk(L.ball(S.FLAG_R13_CRAG))
    expect(L.getFlag(S.FLAG_R13_CRAG) and L.itemCount(S.ITEM_PP_UP) >= 1, "the crag pocket's PP Up")
    climb(47, 13, K.DOWN, 47, 17, "Route 13's scarp, down")
    L.shot("r13_road")
end)
