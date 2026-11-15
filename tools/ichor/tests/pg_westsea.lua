-- Route 33, the western sea: run by tools/ichor/tests/pg_westsea.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap

local function surfing() return emu:read8(S.gPlayerAvatar) & S.PLAYER_AVATAR_FLAG_SURFING ~= 0 end
local function weather() return emu:read8(S.gWeather + S.OFF_WEATHER_CURR) end
local function metatileAt(x, y) local mid = L.grid().tile(x, y) return mid end

local function warp(x, y, header)
  L.setVar(S.VAR_0x8008, x); L.setVar(S.VAR_0x8009, y)
  L.runHeader(header or "WestseaTest_WarpHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE33 and L.idle() end, 3000, "Route 33")
  wait(30)
end
local function give(item, n)
  L.setVar(S.VAR_0x8004, item); L.setVar(S.VAR_0x8005, n or 1)
  L.runHeader("WestseaTest_GiveHeader")
end
-- Press A on what the player faces and play it out.
local function press(answers)
  tap(K.A); wait(8)
  L.settle({ answers = answers })
end
-- One step that the sea may refuse (L.step returns "moved", "blocked" or "taken").
local function step(key) return L.step(key) end

L.start(function()
  L.quickstart()

  -- ---- onto Route 33 by Tainaron's landing, surfing ------------------------------------
  L.setBeat("tainaron", false)
  L.setVar(S.VAR_0x8008, 56); L.setVar(S.VAR_0x8009, 66)
  L.runHeader("WestseaTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE33 and L.idle() end, 3000, "Route 33")
  wait(40)
  L.assistLevel100()
  local x, y = L.pos()
  expect(x == 56 and y == 66 and surfing(), string.format("on Route 33 at Tainaron's landing, surfing (%d,%d)", x, y))
  shot("tainaron")

  -- ---- a mandatory line: Pontia watches the reef fence's north gap ------------------------
  L.setBeat("pontia", false)
  warp(42, 56)
  shot("fence_north_gap")
  expect(not L.defeated(S.TRAINER_ICHOR_PONTIA), "Pontia hasn't battled yet")
  local r = step(K.LEFT)                       -- (41,56): not yet in her line
  r = step(K.LEFT)                             -- (40,56): in it
  expect(r == "taken", "sailing into the gap below Pontia, she spots you (" .. r .. ")")
  L.settle({ limit = 30000 })
  expect(L.defeated(S.TRAINER_ICHOR_PONTIA), "Pontia's battle is fought and won")
  L.runHeader("WestseaTest_HealHeader")

  -- ---- the westward current, closed by loose rock where it cuts the fence ------------------
  L.setBeat("current", false)
  warp(46, 67)
  L.waitUntil(function() local cx = L.pos() return cx == 41 and L.idle() end, 600, "the current to carry you to the rock")
  x, y = L.pos()
  expect(x == 41 and y == 67, string.format("the current carries you west to the loose rock and stops (%d,%d)", x, y))
  shot("current_against_rock")
  L.face(K.LEFT)
  press({ "yes" })
  expect(not L.getFlag(S.FLAG_ICHOR_R33_ROCKS_CHANNEL), "without the bronze ram the rock holds")
  L.setFlag(S.FLAG_ICHOR_SHIP_RAM)
  press({ "yes" })
  expect(not L.getFlag(S.FLAG_ICHOR_R33_ROCKS_CHANNEL), "with the ram but not aboard the Euploia, the rock holds")
  L.setFlag(S.FLAG_ICHOR_ON_SHIP)
  L.face(K.LEFT)
  press({ "yes" })
  expect(L.getFlag(S.FLAG_ICHOR_R33_ROCKS_CHANNEL), "aboard, the bronze ram breaks the rock")
  expect(metatileAt(S.R33_ROCKS_CURRENT_X, S.R33_ROCKS_CURRENT_Y + 1) == S.METATILE_R33_CURRENT_W,
         "the broken rock's cells are current again")
  shot("rock_broken")
  -- now the current runs on, through the fence, all the way to the fog's approach
  L.waitUntil(function() local cx = L.pos() return cx <= 17 and L.idle() end, 1500, "the current's run west")
  x, y = L.pos()
  expect(x <= 17 and y == 67, string.format("the current carries you west through the fence (%d,%d)", x, y))
  shot("current_run")

  -- ---- the fog bank: weather on its approach, its one way through shut ----------------------
  L.setBeat("fog", false)
  warp(16, 66)
  step(K.LEFT); step(K.LEFT); step(K.LEFT)    -- over the fog's approach line at x = 13
  wait(60)
  expect(weather() == S.WEATHER_FOG_HORIZONTAL, string.format("fog comes in on the approach (weather %d)", weather()))
  step(K.LEFT); step(K.LEFT)
  local before = L.pos()
  local rr = step(K.LEFT)
  x, y = L.pos()
  expect(rr == "blocked" and x == before, string.format("the fog bank's way through is shut (%s at %d,%d)", rr, x, y))
  shot("fog_bank")
  L.face(K.LEFT)
  press()
  for _ = 1, 4 do step(K.RIGHT) end
  wait(60)
  expect(weather() ~= S.WEATHER_FOG_HORIZONTAL, string.format("the fog lifts as you sail out (weather %d)", weather()))

  -- ---- an item in the current's eddy -------------------------------------------------------
  L.setBeat("items", false)
  warp(17, 64)
  L.face(K.LEFT)
  press()
  expect(L.getFlag(S.FLAG_ICHOR_ITEM_R33_CURRENT) and L.itemCount(S.ITEM_MAX_REVIVE) == 1,
         "the amphora in the eddy holds a Max Revive")
  -- a hidden item at the foot of Poseidon's stack
  warp(7, 42)
  L.face(K.LEFT)
  press()
  expect(L.getFlag(S.FLAG_ICHOR_HIDDEN_R33_ALTAR) and L.itemCount(S.ITEM_BIG_PEARL) == 1,
         "a Big Pearl hidden at the foot of Poseidon's stack")

  -- ---- the Echinades' whirlpool: Triton's Conch calms it ------------------------------------
  L.setBeat("whirlpool", false)
  L.setFlag(S.TRAINER_FLAGS_START + S.TRAINER_ICHOR_NERITES)    -- past the gap he'd battle you
  local wx, wy = S.R33_WHIRL_ECHINADES_X, S.R33_WHIRL_ECHINADES_Y
  warp(wx, wy + 3)
  rr = step(K.UP)
  rr = step(K.UP)
  x, y = L.pos()
  expect(y == wy + 2, string.format("the whirlpool blocks the gap (%d,%d)", x, y))
  shot("whirlpool")
  L.face(K.UP)
  press({ "yes" })
  expect(not L.getFlag(S.FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES), "without Triton's Conch the whirlpool turns on")
  give(S.ITEM_POSEIDONS_CONCH, 1)
  press({ "yes" })
  expect(not L.getFlag(S.FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES), "Poseidon's Conch alone can't still it")
  L.setFlag(S.FLAG_ICHOR_TRITON_CONCH)
  L.face(K.UP)
  press({ "yes" })
  expect(L.getFlag(S.FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES), "Triton's Conch calms the whirlpool")
  expect(metatileAt(wx, wy) == S.METATILE_R33_SEA, "the whirlpool's cells are open sea now")
  shot("whirlpool_calmed")
  for _ = 1, 3 do step(K.UP) end
  x, y = L.pos()
  expect(y <= wy - 1, string.format("you sail through the Echinades' gap (%d,%d)", x, y))

  -- ---- Kymon, becalmed: tow him home ----------------------------------------------------------
  L.setBeat("kymon", false)
  warp(S.R33_RAFT_SEA_X - 1, S.R33_RAFT_SEA_Y)
  L.face(K.RIGHT)
  shot("kymon_raft")
  tap(K.A); wait(8)
  L.settle({ answers = { "yes" }, limit = 6000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE33 and L.idle() end, 3000, "the tow's end")
  wait(30)
  x, y = L.pos()
  expect(L.getFlag(S.FLAG_ICHOR_R33_KYMON_HOME) and L.itemCount(S.ITEM_PEARL_STRING) == 1,
         "towing Kymon home earns a Pearl String")
  expect(x == S.R33_TOW_X and y == S.R33_TOW_Y, string.format("the tow ends at Halia's jetty (%d,%d)", x, y))
  expect(metatileAt(S.R33_RAFT_HOME_X, S.R33_RAFT_HOME_Y) == S.METATILE_R33_RAFT_L
         and metatileAt(S.R33_RAFT_SEA_X, S.R33_RAFT_SEA_Y) == S.METATILE_R33_SEA,
         "his raft is moored by the jetty, gone from the open sea")
  shot("towed_home")

  -- ---- Halia's hut: ashore by the jetty, in at the door, rest by her hearth -------------------
  L.setBeat("hut", false)
  step(K.LEFT)                                   -- off the water onto the jetty's end
  wait(30)
  x, y = L.pos()
  expect(not surfing(), string.format("ashore on the jetty (%d,%d)", x, y))
  L.go(14, 45)
  step(K.UP)
  L.waitUntil(function() return L.mapId() == S.MAP_HUT and L.idle() end, 600, "Halia's hut")
  wait(30)
  shot("hut")
  emu:write16(L.partyMon(0) + S.OFF_MON_HP, 1)
  L.talk(L.npc("Route33_WesternSea_HaliasHut_EventScript_Halia"), { answers = { "yes" } })
  expect(L.partyHp(0) > 1, "Halia's hearth rests your Pokémon")
  local kymon = L.npc("Route33_WesternSea_HaliasHut_EventScript_Kymon")
  expect(kymon.present, "Kymon is home")
  L.talk(kymon)
  shot("hut_kymon")
  log("done with the western sea")
end)
