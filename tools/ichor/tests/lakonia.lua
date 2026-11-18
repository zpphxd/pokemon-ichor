-- Lakonia's chapter, played through (design/phase4/SCRIPT.md III-5A to III-5J):
-- the Malea crossing, Gytheion at dusk, Route 25 up the Eurotas, Gylippos at
-- the bridge, the helmet in Lampito's kitchen, Iapetos in the lane, the sealed
-- tablet, the Kourodin, the ring, and the goat paths.
local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
for k, v in pairs(dofile(L.OUT .. "lakonia_scripts.lua")) do S.SCRIPTS[k] = v end
local function flag(f, text) L.expect(L.getFlag(f), text) end
local function act3() return L.getVar(S.VAR_ICHOR_ACT3) end
-- Lakonia's Asclepeion, to top the test party's PP up between the long fights
local function heal()
    L.useWarp(S.MAP_LAKONIA_ASCLEPEION)
    L.talk(L.npc("Lakonia_Asclepeion_EventScript_Healer"), {answers = {"yes", "no"}})
    L.useWarp(S.MAP_LAKONIA)
end

L.start(function()
    L.quickstart()
    L.runHeader("Lakonia_SetupHeader")
    L.assistLevel100()

    -- III-5A: the deck, the night at Skandeia, round Malea, Gytheion at dusk
    L.settle()
    L.expect(L.mapId() == S.MAP_GYTHEION, "the Euploia lands at Gytheion")
    flag(S.FLAG_ARRIVED_GYTHEION, "III-5A sets the arrival")
    L.expect(act3() == 7, "landing sets VAR_ICHOR_ACT3 7")
    -- III-5B: the fisherman bails his boat with Kleon's helmet
    L.settle()
    flag(S.FLAG_GYTHEION_DUSK, "III-5B: the fisherman and Alethea on the quay")
    L.shot("gytheion_dusk")
    L.useWarp(S.MAP_GYTHEION_ASCLEPEION)
    L.talk(L.npc("Gytheion_Asclepeion_EventScript_Healer"), {answers = {"yes", "no"}})
    L.expect(L.lastHeal() == S.MAP_GYTHEION, "Gytheion's Asclepeion becomes the respawn")
    L.useWarp(S.MAP_GYTHEION)

    -- III-5C: up the Eurotas
    L.go(15, 0)
    L.leaveEdge("up", S.MAP_ROUTE25)
    L.expect(L.mapId() == S.MAP_ROUTE25, "Gytheion's north gap opens on Route 25")
    L.shot("route25_south")
    L.go(14, 12)
    L.talk(3, 12)                         -- Amyklai's spring
    L.shot("route25_amyklai")
    L.go(3, 3)
    flag(S.FLAG_SAW_LAKONIA, "III-5C: the town without walls comes into view")
    L.go(0, 3)
    L.leaveEdge("left", S.MAP_LAKONIA)
    L.expect(L.mapId() == S.MAP_LAKONIA, "Route 25's west end comes into Lakonia")

    -- III-5D: Gylippos and Alethea at the bridge
    L.go(30, 37)
    flag(S.FLAG_LAKONIA_ARRIVED, "III-5D: Gylippos meets you")
    L.shot("lakonia_agora")
    heal()
    L.expect(L.lastHeal() == S.MAP_LAKONIA, "Lakonia's Asclepeion becomes the respawn")

    -- III-5E and III-5F: the helmet comes off; the Voice in the lane
    L.useWarp(S.MAP_LAMPITO, true)
    L.settle()
    flag(S.FLAG_RHEA_UNMASKED, "III-5E: Rhea unmasks")
    L.settle()
    flag(S.FLAG_IAPETOS_DONE, "III-5F: Gration and Iapetos are beaten")
    L.expect(act3() == 9, "III-5F sets VAR_ICHOR_ACT3 9")
    L.shot("lakonia_lane")

    -- III-5G: what the Pythia said
    L.useWarp(S.MAP_LAMPITO)
    L.talk(L.npc("LakoniaLampito_EventScript_Alethea"), {answers = {"yes"}})
    flag(S.FLAG_READ_TABLET, "III-5G: Alethea reads the tablet")
    L.shot("lampito_kitchen")

    -- III-5H: it hid you once
    L.useWarp(S.MAP_LAKONIA, true)
    L.settle()
    flag(S.FLAG_KOURODIN, "III-5H: Rhea gives Kleon the Kourodin")

    -- III-5I: the ring
    heal()
    L.go(16, 16)
    L.go(16, 15, {trigger = true})
    L.settle({answers = {"yes"}})
    flag(S.FLAG_KLEON_DONE, "III-5I: the clean battle")
    L.expect(act3() == 10, "the ring sets VAR_ICHOR_ACT3 10")
    L.shot("lakonia_ring")

    -- III-5J: the goat paths
    L.go(25, 6)
    L.go(25, 4, {trigger = true})
    L.settle()
    flag(S.FLAG_PARTED, "III-5J: Rhea, Kleon and Alethea take the goat paths")
    L.shot("lakonia_north_road")
end)
