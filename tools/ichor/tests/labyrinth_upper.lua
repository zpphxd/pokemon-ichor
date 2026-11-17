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

L.start(function()
  L.quickstart()
  L.runHeader("Lab_SetupHeader")
  L.assistLevel100()
  expect(L.mapId() == S.MAP_RING1, "the Grand Staircase's way down lands in Ring I")
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
  L.talk(brazier("G"), {answers = {"yes"}})
  expect(L.getFlag(S.FLAG_G) and L.getFlag(S.FLAG_RING1_GATE), "the gate brazier catches and opens the stair")
  expect(collision(30, 25) == 0, "the grate is up over the stair down")
  expect(L.getVar(S.VAR_KNOSSA) >= 6, "Knossa's story moves to Ring II")
  L.talk(L.npc("LabyrinthRing1_EventScript_Akakallis"), {answers = {"yes"}})
  expect(L.defeated(S.TRAINER_AKAKALLIS), "Akakallis tests whoever Ariadne sends")
  shot("r1_gate_open")
end)
