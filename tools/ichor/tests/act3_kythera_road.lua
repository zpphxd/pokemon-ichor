-- Kythera's road, run by tools/ichor/tests/act3_kythera_road.sh (read it first).
--
-- From Skandeia's gate along the Foam Road (the sign, the great herm, Skopas at
-- the cutting's neck, Alethea's dig at Aphrodite's rock, the basin), up the
-- stair to the Spring of Kallirhoe (Alethea and the youth), back down and on
-- past Kassiteros to Paphia (Alethea sails on the honey boat; the temple door
-- and back), the Foam Laurel as Galatea gives it (act3_galatea_gallery.sh plays
-- the temple itself), then north to the Neraida falls: Krenaia refuses one
-- berry, takes three, and gives the Horn of Achelous. VAR_ICHOR_ACT3 is checked
-- at each beat: 2 on the road, 3 at the Laurel, 4 at the Horn. Battles are won
-- by a level-100 team; wild Pokémon are run from.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K = L.S, L.K
for k, v in pairs(dofile(L.OUT .. "kythera_scripts.lua")) do S.SCRIPTS[k] = v end
local expect = L.expect

local function act3() return L.getVar(S.VAR_ICHOR_ACT3) end
local function on(map, what) expect(L.mapId() == map, what .. string.format(" (map %d)", L.mapId())) end

L.start(function()
  L.quickstart()
  L.runHeader("Road_SetupHeader")

  -- The Foam Road, from Skandeia's gate -------------------------------------------------
  L.setVar(S.VAR_0x8008, 62)
  L.setVar(S.VAR_0x8009, 9)
  L.runHeader("Road_WarpFoamRoadHeader")
  on(S.MAP_FOAM_ROAD, "the Foam Road at Skandeia's gate")
  L.shot("01_foam_road_gate")
  L.talk(L.sign("KytheraFoamRoad_EventScript_SignEast"), { shots = { [1] = "02_sign" } })
  L.talk(L.sign("KytheraFoamRoad_EventScript_Herm"), { shots = { [1] = "03_herm", [2] = "03_herm_oil" } })
  expect(not L.getFlag(S.FLAG_HERM_KYTHERA), "the great herm isn't anointed without olive oil")
  expect(act3() == 2, "VAR_ICHOR_ACT3 is 2 on the road")

  -- the cutting: Skopas at the neck, band 2 behind him
  L.go(39, 8)
  L.shot("04_fork")
  L.go(30, 8)
  expect(L.defeated(S.TRAINER_SKOPAS), "Skopas, mandatory at the cutting's neck, was fought")

  -- Aphrodite's rock: Alethea's scene and the first sherd
  expect(not L.goTrigger(L.triggers("KytheraFoamRoad_EventScript_AletheaRock")), "Alethea's scene starts at the beach")
  L.settle({ shots = { [1] = "05_rock_alethea", [5] = "05_rock_trowel", [6] = "05_rock_sherd", [9] = "05_rock_paris" } })
  expect(L.getFlag(S.FLAG_SHERD_PARIS_1), "the first sherd of amphora #11 is dug")
  expect(L.getFlag(S.FLAG_HIDE_ALETHEA_FOAM_ROAD), "Alethea has gone on toward the spring")
  L.shot("06_rock_after")
  L.talk(L.sign("KytheraFoamRoad_EventScript_Basin"), { shots = { [2] = "07_basin" } })

  -- The Spring of Kallirhoe ----------------------------------------------------------------
  L.go(41, 1)
  L.leaveEdge("up", S.MAP_SPRING)
  on(S.MAP_SPRING, "up the stair to the Spring of Kallirhoe")
  L.shot("08_spring")
  expect(not L.goTrigger(L.triggers("KytheraSpringOfKallirhoe_EventScript_AletheaScene")), "Alethea waits at the spring")
  L.settle({ shots = { [1] = "09_spring_alethea", [3] = "09_spring_voice", [9] = "09_spring_happy" } })
  expect(L.getFlag(S.FLAG_SAW_KALLIRHOE), "FLAG_ICHOR_SAW_KALLIRHOE")
  L.talk(L.npc("KytheraSpringOfKallirhoe_EventScript_Youth"), { shots = { [2] = "10_youth" } })
  L.leaveEdge("down", S.MAP_FOAM_ROAD)
  on(S.MAP_FOAM_ROAD, "back down to the Foam Road")

  -- West past Kassiteros to Paphia ------------------------------------------------------
  L.go(4, 8)
  expect(L.defeated(S.TRAINER_KASSITEROS), "Kassiteros, mandatory at the approach, was fought")
  L.shot("11_paphia_road")
  L.leaveEdge("left", S.MAP_PAPHIA)
  on(S.MAP_PAPHIA, "Paphia's east gate")
  L.shot("12_paphia_square")
  expect(not L.goTrigger(L.triggers("KytheraPaphia_EventScript_AletheaSails")), "Alethea waits on the jetty")
  L.settle({ shots = { [1] = "13_jetty_honey_boat", [2] = "13_jetty_temple", [3] = "13_jetty_careful" } })
  expect(L.getFlag(S.FLAG_ALETHEA_SAILED), "Alethea sailed for Knossa")
  L.shot("14_jetty_after")
  expect(act3() == 2, "VAR_ICHOR_ACT3 is still 2 before the Laurel")

  -- the temple's door, and back out
  L.useWarp(S.MAP_TEMPLE)
  on(S.MAP_TEMPLE, "Paphia's temple door")
  L.shot("15_temple_inside")
  L.useWarp(S.MAP_PAPHIA)
  on(S.MAP_PAPHIA, "out of the temple")
  L.shot("16_temple_steps")

  L.runHeader("Road_LaurelHeader")
  expect(act3() == 3, "VAR_ICHOR_ACT3 is 3 with the Foam Laurel")

  -- The Neraida falls ----------------------------------------------------------------------
  L.go(30, 2)
  L.leaveEdge("up", S.MAP_FALLS)
  on(S.MAP_FALLS, "north of Paphia to the Neraida falls")
  L.shot("17_falls_south")
  L.useWarp(S.MAP_MILL)
  L.shot("18_mill")
  L.useWarp(S.MAP_FALLS)
  L.talk(L.npc("KytheraNeraidaFalls_EventScript_Krenaia"),
         { shots = { [1] = "19_krenaia", [3] = "19_krenaia_horn" }, answers = { "yes" } })
  expect(L.defeated(S.TRAINER_MOPSOS), "Mopsos, mandatory at the ford, was fought")
  expect(L.getFlag(S.FLAG_KRENAIA_TOLD), "Krenaia told the laureled player about the falls")
  expect(not L.getFlag(S.FLAG_GOT_HORN), "one berry isn't three: no Horn yet")
  L.runHeader("Road_BerriesHeader")
  L.talk(L.npc("KytheraNeraidaFalls_EventScript_Krenaia"),
         { shots = { [2] = "20_first_fruits", [3] = "20_horn_fills", [5] = "20_horn_given" }, answers = { "yes" } })
  expect(L.getFlag(S.FLAG_GOT_HORN), "FLAG_ICHOR_GOT_HORN_OF_ACHELOUS")
  expect(L.itemCount(S.ITEM_HORN_OF_ACHELOUS) == 1, "the Horn of Achelous is in the bag")
  expect(L.itemCount(S.ITEM_ORAN_BERRY) == 0, "the three berries were taken")
  expect(act3() == 4, "VAR_ICHOR_ACT3 is 4 with the Horn")
  L.shot("21_falls_roar")
end)
