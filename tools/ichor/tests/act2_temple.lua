-- The Three-Act Play check, run by tools/ichor/tests/act2_temple.sh (read it first).
--
-- Plays the Temple of Dionysus as a player would, with key presses on slice_lib's
-- walker (paths come from the live map, people and signs are found by the script
-- they run), and checks the play's state after each beat: VAR_ICHOR_THREE_ACT_PLAY,
-- the mask (VAR_TEMP_1) and entrances (VAR_TEMP_2), trainer flags, the racks',
-- curtains' and god-machine's metatiles, and the rewards.
--
-- Prints "TEMPLE ok ..." per check, "TEMPLE shot ..." per screenshot, and ends with
-- "TEMPLE done"; any failure prints "TEMPLE FAIL: ..." first.

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, settle = L.log, L.expect, L.wait, L.shot, L.settle
for k, v in pairs(dofile(L.OUT .. "temple_scripts.lua")) do S.SCRIPTS[k] = v end
local P = "ThyrsaCity_TempleOfDionysus_EventScript_"

-- The room (tools/ichor/maps/temple_dionysus.py): each door's doorway cell, the
-- tile a wrong entrance sets the player down on, the curtains, the crane's hook.
local DOORS = { { ivy = { 5, 36 } },
                { ivy = { 5, 24 }, crown = { 10, 24 }, goat = { 15, 24 } },
                { ivy = { 5, 12 }, crown = { 10, 12 }, goat = { 15, 12 } } }
local RACK_FRONT = { { 13, 37 }, { 2, 25 }, { 2, 13 } }
local PEGS = { { comic = { 13, 36 } },
               { comic = { 1, 24 }, tragic = { 2, 24 }, satyr = { 3, 24 } },
               { comic = { 1, 12 }, tragic = { 2, 12 }, satyr = { 3, 12 } } }
local CURTAINS = { { { 18, 31 }, { 19, 31 } }, { { 1, 19 }, { 2, 19 } } }
local HOOK = { 10, 8 }
local MASK = { none = 0, comic = 1, tragic = 2, satyr = 3 }

local function mt(x, y) return (L.grid().tile(x, y)) end
local function play() return L.getVar(S.VAR_PLAY) end
local function mask() return L.getVar(S.VAR_MASK) end
local function at(x, y) local px, py = L.pos() return px == x and py == y end
local function favor() return emu:read8(L.ichor() + S.OFF_ICHOR_FAVOR + S.ICHOR_GOD_DIONYSUS) end

local function pegsFull(act, except)
  for m, xy in pairs(PEGS[act]) do
    local full = S["MT_PEG_" .. m:upper()]
    local want = (m == except) and full + 1 or full
    if mt(xy[1], xy[2]) ~= want then return false end
  end
  return true
end

-- Put on a mask at an act's rack: the rack's line, then the menu (COMIC TRAGIC SATYR
-- NONE; Act I's is COMIC NONE).
local function wearMask(act, name)
  L.talk(L.sign(P .. "Rack_Act" .. act), { noSettle = true })
  wait(70); L.logText(); L.tap(K.A)                -- "A rack of masks..."
  L.waitUntil(function() return L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 600, "the mask menu")
  wait(12)
  shot("rack_" .. act .. "_" .. name)
  local downs = (act == 1) and ({ comic = 0, none = 1 })[name] or ({ comic = 0, tragic = 1, satyr = 2, none = 3 })[name]
  for _ = 1, downs do L.tap(K.DOWN) end
  L.tap(K.A)
  L.waitUntil(function() return not L.taskRunning("Task_HandleScrollingMultichoiceInput") end, 120, "the menu to close")
  settle()
  expect(mask() == MASK[name], string.format("wearing %s (VAR_TEMP_1 %d)", name, mask()))
  if name ~= "none" then
    expect(pegsFull(act, name), string.format("Act %d's %s peg shows empty, the rest full", act, name))
  end
end

-- Walk to the tile below a door and step into the doorway; play out what happens.
local function enter(act, door, shotName)
  local d = DOORS[act][door]
  L.go(d[1], d[2] + 1)
  local r = L.step(K.UP)
  expect(r == "taken", string.format("stepping into Act %d's %s door starts the entrance", act, door))
  settle({ shots = shotName and { [1] = shotName } or nil })
end

-- Off the stage and back into the wings through a door: no entrance.
local function backToWings(act, door)
  local d = DOORS[act][door]
  L.go(d[1], d[2] + 1)
  expect(at(d[1], d[2] + 1), string.format("back in Act %d's wings through the %s door", act, door))
end

L.start(function()
  L.quickstart()
  L.runHeader("TempleTest_SetupHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_TEMPLE and L.idle() end, 4000, "the temple")
  wait(30)
  L.setBeat("entry")
  expect(at(10, 47), "arrived on the doormat")
  expect(play() == 0 and mask() == 0, "nothing played, no mask")
  expect(mt(CURTAINS[1][1][1], CURTAINS[1][1][2]) == S.MT_CURTAIN_CLOSED_L, "Act I's curtain is drawn")
  expect(mt(HOOK[1], HOOK[2]) == S.MT_HOOK, "the god-machine's arm is up")
  shot("door")

  -- Lasos calls out on the first step in.
  expect(L.step(K.UP) == "taken", "Lasos's welcome starts inside the door")
  settle({ every = true })
  expect(L.getFlag(S.FLAG_MET_LASOS), "Lasos welcomed the player")
  L.talk(L.npc(P .. "Lasos"), { shots = { [1] = "lasos_again" }, answers = { "yes" } })
  -- The great altar is the engine's (EventScript_IchorTempleAltar_Dionysus): its line,
  -- then the rite's menu; the first choice, PRAY, gives the first Favor of the day.
  L.talk(L.sign(P .. "Altar"), { shots = { [1] = "altar", [2] = "altar_rite" } })
  expect(favor() == 1, "prayed at the great altar: Dionysus Favor 1")
  L.talk(L.npc(P .. "Image"), { shots = { [1] = "image" } })

  -- Act I: the program; a wrong entrance with no mask (Mynniskos stops the player
  -- on the way); the comic mask; the ivy door.
  L.setBeat("act1")
  L.go(10, 39)
  shot("act1_wings")
  L.talk(L.sign(P .. "Program_Act1"), { shots = { [1] = "act1_program" } })
  L.talk(L.sign(P .. "PaintedCrownDoor"), { shots = { [1] = "act1_painted_crown" } })
  L.go(DOORS[1].ivy[1], DOORS[1].ivy[2] + 1)
  expect(L.defeated(S.TRAINER_MYNNISKOS), "Mynniskos battled the player between the rack and the ivy door")
  enter(1, "ivy", "act1_wrong")
  expect(at(RACK_FRONT[1][1], RACK_FRONT[1][2]), "a wrong entrance (no mask) sets the player down by the rack")
  expect(L.getVar(S.VAR_ENTRANCES) == 0 and play() == 0, "a wrong entrance changes nothing")
  wearMask(1, "comic")
  enter(1, "ivy", "act1_right")
  expect(play() == 1, "Act I is done")
  expect(mt(CURTAINS[1][1][1], CURTAINS[1][1][2]) == S.MT_CURTAIN_OPEN_L
         and mt(CURTAINS[1][2][1], CURTAINS[1][2][2]) == S.MT_CURTAIN_OPEN_R, "Act I's curtain drew back")
  shot("act1_stage")

  -- Act II: up the stair; Thettalos in the satyrs' corner (optional); tragic by the
  -- crown door, then comic by the ivy door.
  L.setBeat("act2")
  L.go(18, 27)
  shot("act2_arrival")
  L.talk(L.npc(P .. "Thettalos"), { shots = { [1] = "thettalos" } })
  expect(L.defeated(S.TRAINER_THETTALOS), "beat Thettalos, the optional actor")
  L.talk(L.sign(P .. "Program_Act2"), { shots = { [1] = "act2_program" } })
  wearMask(2, "tragic")
  enter(2, "crown", "act2_crown")
  expect(L.getVar(S.VAR_ENTRANCES) == 1 and play() == 1, "the weeper came on from the king's house")
  backToWings(2, "crown")
  expect(L.getVar(S.VAR_ENTRANCES) == 1, "walking back off the stage is no entrance")
  wearMask(2, "comic")
  enter(2, "ivy", "act2_ivy")
  expect(play() == 2, "Act II is done")
  expect(mt(CURTAINS[2][1][1], CURTAINS[2][1][2]) == S.MT_CURTAIN_OPEN_L, "Act II's curtain drew back")

  -- Act III: comic is waved through by Theodoros; tragic battles him; two wrong
  -- entrances bring the audience's hint; then the satyr by the goat door.
  L.setBeat("act3")
  L.go(2, 15)
  shot("act3_arrival")
  L.talk(L.sign(P .. "Program_Act3"), { every = true })
  wearMask(3, "comic")
  enter(3, "ivy", "act3_ivy")
  expect(not L.defeated(S.TRAINER_THEODOROS), "Theodoros waved the comic mask through")
  expect(L.getVar(S.VAR_ENTRANCES) == 1, "Act III's first entrance: the one who laughs")
  backToWings(3, "ivy")
  wearMask(3, "tragic")
  enter(3, "crown", "act3_crown")
  expect(L.defeated(S.TRAINER_THEODOROS), "Theodoros battled the tragic mask")
  expect(L.getVar(S.VAR_ENTRANCES) == 2, "Act III's second entrance: the one who weeps")
  backToWings(3, "crown")
  enter(3, "ivy", "act3_wrong_1")
  enter(3, "crown", "act3_wrong_2")
  expect(L.getVar(S.VAR_MISSES) == 2, "two wrong entrances in Act III")
  expect(L.getVar(S.VAR_ENTRANCES) == 2, "wrong entrances keep the act's place")
  wearMask(3, "satyr")
  enter(3, "goat", "act3_goat")
  expect(play() == 3 and L.getFlag(S.FLAG_PLAY_DONE), "the play is done")
  expect(mt(HOOK[1], HOOK[2]) == S.MT_HOOK_LOWERED and mt(10, 2) == S.MT_MAST_TOP_LOWERED
         and mt(10, 4) == S.MT_ARM_LOWERED, "the god-machine's arm swung down")
  shot("act3_machine")

  -- The god-machine, the roof, Thespis.
  L.setBeat("thespis")
  L.talk(L.sign(P .. "Hook"), { noSettle = true })
  wait(60); shot("hook_prompt")
  settle({ shots = { [3] = "roof_entrance", [6] = "roof_prosomime" }, limit = 60000 })
  expect(L.defeated(S.TRAINER_THESPIS), "beat Thespis")
  expect(L.getFlag(S.FLAG_BADGE04_GET), "the Mask Laurel")
  expect(L.getFlag(S.FLAG_GOT_TM_TOXIC) and L.itemCount(S.ITEM_TM_TOXIC) == 1, "TM06 Toxic")
  expect(L.getFlag(S.FLAG_CRATER), "the Crater on the Star Chart")
  expect(favor() == 16, "the laurel: Dionysus Favor +15 (16 with the prayer)")
  expect(L.itemCount(S.ITEM_WINE) == 1 and L.getFlag(S.FLAG_HIEROPHANT_OFFERING),
         "the Hierophant's rite: one Wine, his offering's flag set")
  expect(play() == 5, "the play's state is the laurel given")
  expect(L.mapId() == S.MAP_TEMPLE and at(10, 46), "set down inside the door")
  local t = L.npc(P .. "Thespis")
  expect(t.x == 13 and t.y == 44, "Thespis stands by the altar")
  shot("after_laurel")
  L.talk(t, { shots = { [1] = "thespis_after" } })
  L.talk(L.npc(P .. "Lasos"), { shots = { [2] = "lasos_after" } })

  -- Back in through the door: the room stays solved.
  L.setBeat("reentry")
  L.runHeader("TempleTest_ReenterHeader", { noSettle = true })
  L.waitUntil(function() return L.mapId() == S.MAP_TEMPLE and L.idle() and at(10, 47) end, 4000, "the temple again")
  wait(30)
  expect(play() == 5 and mask() == 0, "re-entered: the play stays done, no mask")
  expect(mt(CURTAINS[1][1][1], CURTAINS[1][1][2]) == S.MT_CURTAIN_OPEN_L
         and mt(CURTAINS[2][1][1], CURTAINS[2][1][2]) == S.MT_CURTAIN_OPEN_L
         and mt(HOOK[1], HOOK[2]) == S.MT_HOOK_LOWERED, "re-entered: the curtains open, the machine down")
  L.go(10, 39)
  L.talk(L.sign(P .. "Program_Act1"), { shots = { [1] = "program_fin" } })
  L.go(12, 33)
  shot("reentry_act1_stage")
  log("ok " .. L.bugs .. " bugs")
end)
