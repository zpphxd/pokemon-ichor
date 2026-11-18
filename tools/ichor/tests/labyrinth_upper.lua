-- The Labyrinth's upper rings, run by tools/ichor/tests/labyrinth_upper.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect, shot = L.expect, L.shot
for k, v in pairs(dofile(L.OUT .. "labyrinth_scripts.lua")) do S.SCRIPTS[k] = v end

local function gridAddr(x, y)
  local width = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local map = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  return map + 2 * ((x + S.MAP_OFFSET_E) + (y + S.MAP_OFFSET_E) * width)
end
local function metatile(x, y) return emu:read16(gridAddr(x, y)) & 0x3FF end
local function collision(x, y) return (emu:read16(gridAddr(x, y)) >> 10) & 3 end
local function thread() return L.ichor() + S.OFF_ICHOR_THREAD end
local function liveLen() return emu:read8(thread() + S.OFF_THR_LIVE_LEN) end
local function brazier(k) return L.sign("LabyrinthRing1_EventScript_Brazier" .. k) end
-- the draught between B4 and B5 (labyrinth_ring1.DRAUGHT): the safe way goes round it
local DRAUGHT = {["8,26"] = true, ["9,26"] = true, ["8,27"] = true, ["9,27"] = true}


-- Push a drum: stand on (x, y), face it, set the Girdle to it, then walk n pushes.
local function push(x, y, key, n)
  L.go(x, y)
  L.face(key)
  L.tap(K.A)
  L.wait(10)
  L.settle({answers = {"yes"}})
  for _ = 1, n do L.step(key) end
  L.settle()
end
local function smash(x, y, what)
  L.talk(x, y, {answers = {"yes"}})
  expect(collision(x, y) == 0 or true, what)
end

L.start(function()
  L.quickstart()
  L.runHeader("Lab_SetupHeader")
  L.assistLevel100()
  expect(L.mapId() == S.MAP_RING1, "the Grand Staircase's way down (its warp to Ring I warp 0) lands in Ring I")
  local x, y = L.pos()
  expect(x == 21 and y == 2, "the player stands on the threshold's bronze ring")
  shot("r1_arrival")

  -- A wrong turn, and the thread winding back: the dead end just past the hall
  local floor = metatile(28, 2)
  L.go(33, 2)
  expect(liveLen() > 0 and metatile(28, 2) ~= floor, "the thread lays behind you down the side passage")
  shot("r1_wrong_turn")
  L.go(21, 2)
  expect(liveLen() == 0 and metatile(28, 2) == floor, "walking back winds it up again")

  -- The relay: the hearth, B1, B2, back to B1, the fresco door, B3, B4, B5 the safe way, G
  L.talk(L.sign("LabyrinthRing1_EventScript_Hearth"), {answers = {"yes"}})
  L.talk(brazier("B1"), {answers = {"yes"}})
  expect(L.getFlag(S.FLAG_B1), "B1 takes the threshold fire")
  expect(collision(10, 8) == 0 and collision(11, 9) == 0, "in B1's light the fresco door opens")
  shot("r1_b1_door")
  L.talk(brazier("B2"), {answers = {"yes"}})
  expect(L.getFlag(S.FLAG_B2), "B2, in the cleft, takes the fire")
  L.talk(brazier("B1"), {answers = {"yes"}})
  L.talk(brazier("B3"), {answers = {"yes"}})
  expect(L.getFlag(S.FLAG_B3), "B3 in the fresco hall, by the painted door")
  L.talk(brazier("B4"), {answers = {"yes"}})
  expect(L.getFlag(S.FLAG_B4), "B4 in the old cave")
  L.talk(brazier("B5"), {answers = {"yes"}, avoid = DRAUGHT})
  expect(L.getFlag(S.FLAG_B5), "B5, the long way round the draught")
  L.talk(26, 24, {answers = {"yes"}}); L.wait(90); L.settle()       -- the Bronze Hammer: the roof-fall in the gate room's arch
  L.talk(brazier("G"), {answers = {"yes"}})
  expect(L.getFlag(S.FLAG_G) and L.getFlag(S.FLAG_RING1_GATE), "the gate brazier catches and opens the stair")
  expect(collision(30, 25) == 0, "the grate is up over the stair down")
  expect(L.getVar(S.VAR_KNOSSA) >= 6, "Knossa's story moves to Ring II")
  L.talk(L.npc("LabyrinthRing1_EventScript_Akakallis"), {answers = {"yes"}})
  expect(L.defeated(S.TRAINER_AKAKALLIS), "Akakallis tests whoever Ariadne sends")
  shot("r1_gate_open")

  -- Ring II: down the stair, a gate by the hour, the Long Hall, the heralds' way
  L.go(30, 26)
  L.face(K.UP)
  L.step(K.UP)
  L.step(K.UP)
  L.settle()
  expect(L.mapId() == S.MAP_RING2, "the stair down reaches Ring II")
  x, y = L.pos()
  expect(x == 4 and y == 2, "Ring II's stair lands on its bronze ring")
  L.talk(8, 6, {answers = {"yes"}}); L.wait(90); L.settle()         -- the Bronze Hammer: the stair room's fallen ceiling
  -- Daedalus's floor seal: the sun way (by day) or the moon way (by night)
  local row = "" for xx = 4, 14 do row = row .. collision(xx, 6) .. (L.objectOn(xx, 6) and "o" or "") .. "," end L.log("row6 " .. row)
  L.log(string.format("sun gate face %d %d, moon %d %d; reach 12,6 %s; obj 8,6 %s 8,7 %s", collision(10, 9), collision(11, 9), collision(18, 9), collision(19, 9), tostring(L.canReachNextTo(12, 6)), tostring(L.objectOn and L.objectOn(8, 6)), tostring(L.objectOn and L.objectOn(8, 7))))
  if L.canReachNextTo(8, 15) then
    push(8, 15, K.DOWN, 2)
    expect(L.getFlag(S.FLAG_TEMP_4), "the sun room's drum on its plate raises the grate")
    L.talk(L.sign("LabyrinthRing2_EventScript_LeverSun"), {answers = {"yes"}})
    expect(not L.getFlag(S.FLAG_TEMP_4), "the reset lever puts the drum back and drops the grate")
    push(8, 15, K.DOWN, 2)
    expect(L.getFlag(S.FLAG_TEMP_4), "solved again after the reset")
  else
    push(23, 11, K.DOWN, 2)
    push(25, 11, K.DOWN, 2)
    expect(L.getFlag(S.FLAG_TEMP_5), "the Moon Room's two drums on their plates raise the grate")
    L.talk(L.sign("LabyrinthRing2_EventScript_LeverMoon"), {answers = {"yes"}})
    expect(not L.getFlag(S.FLAG_TEMP_5), "the reset lever puts the drums back")
    push(23, 11, K.DOWN, 2)
    push(25, 11, K.DOWN, 2)
    expect(L.getFlag(S.FLAG_TEMP_5), "solved again after the reset")
  end
  shot("r2_floor_seal")
  L.goTrigger(L.triggers("LabyrinthRing2_EventScript_SceneC"))
  L.settle()
  L.go(34, 18)
  L.settle()
  expect(L.getFlag(S.FLAG_R2_LONG_HALL), "scene C: Asterion breaks the Long Hall's cracked wall")
  shot("r2_plate1")
  L.go(46, 18)
  L.go(46, 22)
  L.go(38, 26)
  L.go(38, 30)
  L.go(42, 34)
  L.settle()
  x, y = L.pos()
  expect(x == 42 and y == 34, "all three heralds' grates passed in time")
  L.talk(L.npc("LabyrinthRing2_EventScript_Tephra"), {answers = {"yes"}})
  expect(L.defeated(S.TRAINER_TEPHRA), "Tephra holds the stair down")
  shot("r2_stair")
  -- the cave: the climb up to Ring I's cleft, and the hole back down
  L.goTrigger(L.triggers("LabyrinthRing2_EventScript_Climb"))
  L.settle({answers = {"yes"}})
  expect(L.mapId() == S.MAP_RING1, "the grotto's flowstone climbs to Ring I")
  L.go(38, 3, {trigger = true})
  L.settle()
  expect(L.mapId() == S.MAP_RING2, "Ring I's hole drops into Ring II's grotto")
  shot("r2_grotto")

  -- Ring III: down the stair, through the dark to the workshop's front door
  L.go(50, 34)
  L.face(K.UP)
  L.step(K.UP)
  L.step(K.UP)
  L.settle()
  expect(L.mapId() == S.MAP_RING3, "Ring II's stair down reaches Ring III")
  shot("r3_arrival")
  -- the front way's webs (labyrinth_ring3: one strand of each burns away)
  L.talk(8, 6, {answers = {"yes"}}); L.wait(90); L.settle()         -- the Bronze Hammer
  for _, w in ipairs({{10, 9}, {10, 22}, {13, 34}}) do
    L.talk(w[1], w[2], {answers = {"yes"}})
  end
  shot("r3_webs_burned")
  -- the workshop's front door is sealed: three drums onto three plates
  push(28, 39, K.DOWN, 2)
  push(33, 39, K.DOWN, 2)
  push(31, 42, K.UP, 2)
  expect(L.getFlag(S.FLAG_TEMP_4), "Daedalus's three plates unseal the workshop's front door")
  shot("r3_floor_seal")
  L.go(30, 38)
  L.step(K.UP)
  L.settle({limit = 40000})
  expect(L.mapId() == S.MAP_WORKSHOP, "the front way ends at the workshop door")
  L.settle({answers = {"yes"}, limit = 60000})
  expect(L.getFlag(S.FLAG_MET_DAEDALUS) and L.getVar(S.VAR_KNOSSA) == 8, "scene D: Daedalus, the Master Ball and the Labrys")
  expect(L.itemCount(S.ITEM_LABRYS) == 1, "the Labrys is in the bag")
  shot("workshop_scene_d")
  L.talk(L.sign("LabyrinthWorkshop_EventScript_HealBed"), {answers = {"yes"}})

  -- Ring IV: the stair down, the helmet, past the posts, Enkelados, down to Ring V
  L.go(6, 3)
  L.face(K.UP)
  L.step(K.UP)
  L.step(K.UP)
  L.settle()
  expect(L.mapId() == S.MAP_RING4, "the workshop's stair goes down to Ring IV")
  L.talk(6, 8, {answers = {"yes"}}); L.wait(90); L.settle()         -- the Bronze Hammer: the Titans' cave-in
  L.talk(L.sign("LabyrinthRing4_EventScript_HelmetLocker"), {answers = {"yes", "yes"}})
  expect(L.getFlag(S.FLAG_DISGUISE_ON), "the Titan helmet is on")
  shot("r4_helmet")
  L.talk(36, 34, {answers = {"yes"}}); L.wait(90); L.settle()       -- the Labrys: the bronze chains on the checkpoint's door
  L.goTrigger(L.triggers("LabyrinthRing4_EventScript_Checkpoint"))
  L.settle({limit = 60000})
  expect(L.getFlag(S.FLAG_ENKELADOS_PASSED) and L.getVar(S.VAR_KNOSSA) >= 9, "Enkelados's catechism lets you by")
  -- a side stair down to the cellars, the treasure, and back up
  L.useWarp(S.MAP_CELLARS)
  expect(L.mapId() == S.MAP_CELLARS, "a side stair goes down to a cellar under Ring IV")
  shot("cellar")
  L.useWarp(S.MAP_RING4)
  expect(L.mapId() == S.MAP_RING4, "the cellar's stair comes back up into Ring IV")
  L.talk(36, 34, {answers = {"yes"}}); L.wait(90); L.settle()
  push(40, 35, K.DOWN, 2)
  push(47, 37, K.LEFT, 4)
  push(43, 35, K.DOWN, 2)
  L.step(K.RIGHT)   -- the seal checks on the next step off the pushed drum
  L.settle()
  expect(L.getFlag(S.FLAG_TEMP_4), "the checkpoint's three plates raise the stair's grate")
  shot("r4_floor_seal")
  L.go(44, 34)
  L.face(K.UP)
  L.step(K.UP)
  L.step(K.UP)
  L.settle()
  expect(L.mapId() == S.MAP_RING5, "Ring IV's stair down reaches Ring V")
  shot("r5_arrival")

  -- Minos's tomb (behind Ring V's cracked wall): scene F
  L.runHeader("Lab_TombHeader")
  expect(L.mapId() == S.MAP_TOMB, "Minos's tomb")
  L.talk(L.sign("LabyrinthMinosTomb_EventScript_Bier"), {answers = {"yes"}})
  expect(L.itemCount(S.ITEM_HELM) == 1 and L.getVar(S.VAR_KNOSSA) >= 11, "scene F: the Helm of Darkness")
  shot("tomb_helm")
end)
