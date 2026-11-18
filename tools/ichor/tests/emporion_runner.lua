-- The road to Astyra after the Moon Laurel, run by tools/ichor/tests/emporion_runner.sh
-- (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect, shot = L.expect, L.shot
for k, v in pairs(dofile(L.OUT .. "runner_symbols.lua")) do S.SCRIPTS[k] = v end

local RUNNER = "EmporionCity_EventScript_HermRunner"
local LAND_X, LAND_Y = 19, 41            -- Emporion's herm landing; the herm is south of it
local DIR_SOUTH = 1

local function runner() return L.npc(RUNNER) end

-- Into Emporion by the Nemea Gate, then up the road to the runner's trigger.
local function walkIn()
  L.runHeader("Runner_MoonHeader")
  expect(L.mapId() == S.MAP_R14, "starts on Route 14's east end")
  L.leaveEdge("right", S.MAP_EMPORION)
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_EMPORION and y == 41, string.format("crossed into Emporion by the Nemea Gate at (%d,%d)", x, y))
  shot("nemea_gate")
  expect(not L.getFlag(S.FLAG_HIDE_RUNNER), "the runner is out after the Moon Laurel")
  local r = runner()
  expect(r.x == 20 and r.y == 41, string.format("she waits beside the herm, at (%d,%d)", r.x, r.y))
  expect(L.go(2, 41, { trigger = true }) == false, "the Nemea road's trigger starts the scene")
end

L.start(function()
  L.quickstart()

  -- --- YES: the runner walks the player to the herm, and the herm takes them to Eleusa
  walkIn()
  expect(emu:saveStateFile(L.OUT .. "scene_start.ss", 31), "saved the scene's start for the NO branch")
  -- every box is shot, and the walk to the herm once halfway along the road
  local walked = false
  L.settle({ answers = { "yes" }, every = true,
             stop = function()
               local px = L.pos()
               if not walked and L.mapId() == S.MAP_EMPORION and px == 10 then walked = true; shot("walk_to_herm") end
               return L.mapId() == S.MAP_ELEUSA and L.idle()
             end })
  expect(walked, "the runner walked the player along the Nemea road")
  L.settle()
  local x, y = L.pos()
  expect(L.mapId() == S.MAP_ELEUSA and x == 5 and y == 24,
         string.format("YES lands on Eleusa's herm tile (map %d at %d,%d)", L.mapId(), x, y))
  expect(L.getFlag(S.FLAG_TOLD), "the scene is marked played")
  expect(L.getFlag(S.FLAG_HERM_ELEUSA), "Eleusa's herm is registered for a player who had been there")
  shot("eleusa_landing")
  -- a player who reaches Eleusa another way still hears where the road goes
  expect(not L.npc("EleusaVillage_EventScript_Hoplite").present, "the road's old watch post is empty")
  local watch = L.npc("EleusaVillage_EventScript_WatchAside")
  expect(watch.x == 47 and watch.y == 23, "the watch stands aside, off the open road")
  L.talk(L.npc("EleusaVillage_EventScript_WatchAside"), { every = true })
  shot("eleusa_watch_aside")
  L.leaveEdge("right", S.MAP_R15)
  expect(L.mapId() == S.MAP_R15, "the east road is open to Route 15")

  -- --- NO: the player stays at the herm, the runner beside it, and nothing replays
  expect(emu:loadStateFile(L.OUT .. "scene_start.ss", 31), "back to the scene's start")
  L.wait(10)
  L.settle({ answers = { "no" }, every = true })
  x, y = L.pos()
  expect(L.mapId() == S.MAP_EMPORION and x == LAND_X and y == LAND_Y and L.facing() == DIR_SOUTH,
         string.format("NO leaves the player at the herm, facing it (%d,%d)", x, y))
  local r = runner()
  expect(r.present and r.x == 20 and r.y == 41, "the runner waits beside the herm")
  expect(L.getFlag(S.FLAG_TOLD), "the scene is marked played after NO too")
  shot("no_at_the_herm")
  L.talk(runner(), { answers = { "no" }, every = true })
  expect(L.mapId() == S.MAP_EMPORION and L.idle(), "asking her again re-offers, and NO lets go")
  expect(L.go(2, 41, { trigger = true }) == true, "the Nemea road's trigger is spent")
  L.go(3, 41)
  expect(L.idle(), "no replay on the way back to the gate")
  L.talk(runner(), { answers = { "yes" } })
  L.settle()
  x, y = L.pos()
  expect(L.mapId() == S.MAP_ELEUSA and x == 5 and y == 24, "her later offer travels to Eleusa too")

  -- --- By the herm instead: she tells the player where they land
  L.runHeader("Runner_LandHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_EMPORION end, 600, "Emporion's herm")
  L.waitUntil(function() return not L.idle() end, 300, "the landing scene")
  L.settle({ answers = { "no" }, every = true })
  x, y = L.pos()
  expect(L.getFlag(S.FLAG_TOLD) and L.mapId() == S.MAP_EMPORION and x == LAND_X and y == LAND_Y,
         "landing at the herm plays the news there, and NO stays")
  shot("landing_after")
  L.log("done")
end)
