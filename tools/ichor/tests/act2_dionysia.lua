-- The Dionysia check, run by tools/ichor/tests/act2_dionysia.sh (read it first).
--
-- Plays beats 32-34 in Thyrsa's theater with key presses, from a save just
-- after the Three-Act Play, and checks the play's stage (VAR_ICHOR_DIONYSIA),
-- the mask worn, the story flags, the trainer flags, the trance's palettes and
-- the Girdle. Every message box is screenshotted, in order, for the look review.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, tap, shot = L.log, L.expect, L.wait, L.tap, L.shot
for k, v in pairs(dofile(L.OUT .. "theater_scripts.lua")) do S.SCRIPTS[k] = v end

local TH, SK = "ThyrsaTheater_EventScript_", "ThyrsaTheater_Skene_EventScript_"

local function stage() return L.getVar(S.VAR_DIONYSIA) end

-- A menu is up (a multichoice, a scrolling one, or a dynamic one).
local function menuUp()
  return L.taskRunning("Task_HandleMultichoiceInput") or L.taskRunning("Task_HandleScrollingMultichoiceInput")
end

-- Press A through messages until a menu opens.
local function untilMenu(limit)
  local t0, stalled = L.now(), 0
  while not menuUp() do
    if L.boxUp() or (L.inOverworld() and L.newText()) then
      wait(30)
      if not menuUp() then
        L.logText()
        shot("text")
        tap(K.A)
      end
      wait(4)
      stalled = 0
    else
      wait(2)
      stalled = stalled + 2
      -- a box that finished printing under the last A press waits for another
      if stalled >= 40 and L.scriptRunning() then
        tap(K.A)
        stalled = 0
      end
    end
    if L.now() - t0 > (limit or 3000) then L.fail("no menu opened (" .. L.where() .. ")") end
  end
  wait(10)
end

-- Pick the nth option (0 first) of the open menu.
local function choose(n, name)
  shot("menu_" .. (name or n))
  for _ = 1, n do tap(K.DOWN) end
  tap(K.A)
  L.waitUntil(function() return not menuUp() end, 120, "the menu to close")
end

-- Walk to (x, 3) under a door in the wings, then into it: an entrance.
local function enterDoor(x, label)
  L.go(x, 3)
  emu:addKey(K.UP); wait(20); emu:clearKey(K.UP)
  L.waitUntil(function() return L.mapId() == S.MAP_THEATER end, 900, "the stage, through the " .. label .. " door")
end

-- The pairs of blocks' palettes in palette RAM: is pair p's tinted away from the
-- crowd's own palette (slot 6, which never pulses)?
local CROWD, PAIRS = 6, { low = 10, mid = 11, top = 12 }
local function tinted(slot)
  local diff = 0
  for i = 1, 15 do
    if emu:read16(0x05000000 + CROWD * 32 + i * 2) ~= emu:read16(0x05000000 + slot * 32 + i * 2) then
      diff = diff + 1
    end
  end
  return diff > 4
end

L.start(function()
  L.quickstart()
  L.setBeat("32_setup", false)
  L.runHeader("Dionysia_SetupHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_THEATER and L.idle() end, 3000, "the theater")
  wait(30)
  shot("arrival_workers")
  expect(stage() == 0, "the theater before the play: the workers sweep, nothing has begun")
  expect(L.npc(TH .. "Worker").present, "a worker sweeps the promenade")

  -- Beat 32: the first step down the central stair begins the play
  L.setBeat("32_play", false)
  L.goTrigger(L.triggers(TH .. "TakeYourSeat"))
  L.settle({ every = true, limit = 60000 })
  expect(L.getFlag(S.FLAG_DIONYSIA_BEGUN), "FLAG_ICHOR_DIONYSIA_BEGUN is set")
  expect(L.mapId() == S.MAP_SKENE, "Silenos called them backstage: the player is in the skene")
  expect(stage() == S.DIONYSIA_ENTRANCE_1, string.format("Thespis's scene leaves the entrances open (stage %d)", stage()))
  shot("wings")

  -- A wrong entrance: no mask, through the goat door
  L.setBeat("32_wrong", false)
  enterDoor(15, "goat")
  L.waitUntil(L.inOverworld, 600, "the theater's field")
  wait(60)
  shot("wrong_entrance_stage")
  L.check(tinted(PAIRS.low) and tinted(PAIRS.mid) and tinted(PAIRS.top),
          "the trance: all three pairs of blocks pulse violet before the first laugh")
  L.settle({ every = true })
  expect(L.mapId() == S.MAP_SKENE and stage() == S.DIONYSIA_ENTRANCE_1,
         "a wrong entrance: nobody laughs, and the player is back in the wings")

  -- 1. The comic mask by the ivy door
  L.setBeat("32_comic", false)
  L.talk(L.sign(SK .. "Rack"), { noSettle = true })
  untilMenu()
  choose(0, "comic")
  L.settle()
  expect(L.getVar(S.VAR_MASK) == 1, "the comic mask is on")
  enterDoor(4, "ivy")
  L.settle({ every = true })
  expect(stage() == S.DIONYSIA_ENTRANCE_2, string.format("the comic entrance lands (stage %d)", stage()))
  expect(L.mapId() == S.MAP_SKENE and L.getVar(S.VAR_MASK) == 1, "... back in the wings, still in the comic mask")

  -- 2. The tragic mask by the palace door
  L.setBeat("32_tragic", false)
  L.talk(L.sign(SK .. "Rack"), { noSettle = true })
  untilMenu()
  choose(1, "tragic")
  L.settle()
  enterDoor(9, "palace")
  L.waitUntil(L.inOverworld, 600, "the theater's field")
  wait(60)
  shot("tragic_stage")
  L.check(not tinted(PAIRS.low) and tinted(PAIRS.mid) and tinted(PAIRS.top),
          "after the first laugh: the low pair has stopped pulsing, the others haven't")
  L.settle({ every = true })
  expect(stage() == S.DIONYSIA_ENTRANCE_3, string.format("the tragic entrance lands (stage %d)", stage()))
  expect(L.getFlag(S.FLAG_HIDE_CHORUS_LEADER), "the chorus leader has backed into the palace door")

  -- 3. The satyr mask by the goat door: the trance breaks, the actor fights
  L.setBeat("32_satyr", false)
  L.talk(L.sign(SK .. "Rack"), { noSettle = true })
  untilMenu()
  choose(2, "satyr")
  L.settle()
  enterDoor(15, "goat")
  L.settle({ every = true, limit = 60000 })
  expect(L.mapId() == S.MAP_THEATER, "the play ends on the stage")
  expect(L.defeated(S.TRAINER_BORBOROS), "the actor in the petasos (Borboros) was beaten")
  expect(L.getFlag(S.FLAG_DIONYSIA_DONE), "FLAG_ICHOR_DIONYSIA_DONE is set")
  expect(L.getFlag(S.FLAG_SAW_PROGRAM_HOOK), "FLAG_ICHOR_SAW_PROGRAM_HOOK is set")
  expect(stage() == S.DIONYSIA_OVER, "the theater stands empty, Kleon to come")
  L.check(not tinted(PAIRS.low) and not tinted(PAIRS.mid) and not tinted(PAIRS.top),
          "the purple has drained out of every pair")
  shot("after_the_play")

  -- Beat 33: out through the skene and back in; Kleon waits on the stage's edge
  L.setBeat("33_kleon", false)
  L.useWarp(S.MAP_SKENE)
  L.useWarp(S.MAP_THEATER)
  wait(30)
  expect(L.npc(TH .. "KleonEmpty").present, "Kleon sits on the stage's edge")
  shot("kleon_waits")
  L.goTrigger(L.triggers(TH .. "KleonApproach"))
  L.settle({ every = true, limit = 40000 })
  expect(L.getFlag(S.FLAG_KLEON_BATTLE_3_DONE), "FLAG_ICHOR_KLEON_BATTLE_3_DONE is set")
  expect(L.defeated(S.TRAINER_KLEON_3_KYNDER), "Kleon's Kynder team (KLEON_3_KYNDER) was the one fought")
  expect(L.getFlag(S.FLAG_WON_KLEON_3), "FLAG_ICHOR_WON_KLEON_3 is set after a win")
  expect(stage() == S.DIONYSIA_EMPTY, "the theater is empty")
  shot("empty_theater")

  -- Beat 34: Silenos's riddle and fight
  L.setBeat("34_silenos", false)
  L.useWarp(S.MAP_SKENE)
  L.go(4, 10)                      -- through the arch: the prop room is off-screen from the back door
  local silenos = L.npc(SK .. "Silenos")
  expect(silenos.present, "Silenos sits on his chest in the prop room")
  L.talk(silenos, { noSettle = true })
  untilMenu()
  choose(1, "riddle")
  untilMenu()
  choose(0, "a_road")              -- wrong: a new riddle
  untilMenu()
  choose(2, "footsteps")           -- right
  L.settle({ every = true })
  expect(L.getFlag(S.FLAG_SILENOS_WON_RIDDLE), "the riddle is won (one miss, then FOOTSTEPS)")
  expect(not L.getFlag(S.FLAG_GOT_GIRDLE), "one win isn't the Girdle")
  L.talk(silenos, { noSettle = true })
  untilMenu()
  choose(1, "fight")               -- the menu is now BONES, A FIGHT, NOT NOW
  L.settle({ every = true, limit = 40000 })
  expect(L.defeated(S.TRAINER_SILENOS), "Silenos was beaten")
  expect(L.getFlag(S.FLAG_SILENOS_WON_FIGHT), "the fight is won")
  expect(L.getFlag(S.FLAG_GOT_GIRDLE), "two of three: FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES is set")
  expect(L.getFlag(S.FLAG_DAEDALUS_PAGE_3), "Daedalus's page III is set")
  shot("girdle")
  L.talk(silenos, { every = true })
  shot("silenos_after")
  log("ok " .. L.bugs .. " bugs")
  if L.bugs > 0 then L.fail(L.bugs .. " checks failed") end
end)
