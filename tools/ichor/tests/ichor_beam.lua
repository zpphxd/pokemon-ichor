-- The beam trace, run by tools/ichor/tests/ichor_beam.sh (read it first).
--
-- In the Agora: a source mirror SRC at (1,6) facing east (the light falls on
-- it), a mirror M at (9,6) facing north, and a target T at (9,3). Floor on
-- row 6, and on (9,4)-(9,5) and (9,7)-(9,8). The player stands at (4,6), on
-- the beam's path (the player doesn't block a beam). The six beam metatiles
-- are placeholders from BASE.
--   1. SRC traced: the beam runs east to M, turns north, and ends on T.
--      VAR_RESULT is T's local id; the floor became the east-west piece, the
--      north-west corner under M, then the north-south piece.
--   2. M turned south (`turnobject`) and SRC traced again: the old path's
--      north leg is floor again, the corner is south-west, the beam runs south
--      to the map's edge: VAR_RESULT 0.
--   3. M turned east, its back to the beam: the beam ends on M.
--   4. M turned west, facing the beam head-on: the beam ends on M.
--   5. M turned north again: the beam reaches T again.

local L = dofile("tools/ichor/tests/act3_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect = L.expect

local BASE = 0x3F0
local EW, NS, NE, NW, SE, SW = BASE, BASE + 1, BASE + 2, BASE + 3, BASE + 4, BASE + 5
local src, mirror, target, floor

local function trace()
  L.setVar(S.VAR_0x8004, src)
  L.setVar(S.VAR_0x8005, BASE)
  emu:write16(S.gSpecialVar_Result, 0xFFFF)
  L.runHeader("Act3Test_BeamHeader")
  return emu:read16(S.gSpecialVar_Result), L.getVar(S.VAR_0x8006), L.getVar(S.VAR_0x8007)
end
local function turnMirror(header)
  L.setVar(S.VAR_0x8000, mirror)
  L.runHeader(header)
end
local function expectRow(x0, x1, y, mt, what)
  for x = x0, x1 do
    if L.metatile(x, y) ~= mt then
      L.fail(string.format("%s: (%d,%d) holds metatile %03X, expected %03X", what, x, y, L.metatile(x, y), mt))
    end
  end
  expect(true, what)
end
local function expectColumn(x, y0, y1, mt, what)
  for y = y0, y1 do
    if L.metatile(x, y) ~= mt then
      L.fail(string.format("%s: (%d,%d) holds metatile %03X, expected %03X", what, x, y, L.metatile(x, y), mt))
    end
  end
  expect(true, what)
end
local function expectFloor(x, y, what)
  expect(L.block(x, y) == floor, string.format("%s: (%d,%d) holds %04X, the floor is %04X", what, x, y, L.block(x, y), floor))
end
local function expectEnd(r, x, y, id, what)
  expect(r[1] == id and r[2] == x and r[3] == y,
         string.format("%s: ended at (%d,%d) on %d, expected (%d,%d) on %d", what, r[2], r[3], r[1], x, y, id))
end

L.start(function()
  L.quickstart()
  L.toSpot(4, 6)
  local open = L.row(0, 12, 6)
  for _, t in ipairs({ { 9, 3 }, { 9, 4 }, { 9, 5 }, { 9, 7 }, { 9, 8 } }) do open[#open + 1] = t end
  floor = L.arena(open)
  local ids = L.place{
    { 1, 6, S.MOVEMENT_TYPE_ICHOR_MIRROR_RIGHT },
    { 9, 6, S.MOVEMENT_TYPE_ICHOR_MIRROR_UP },
    { 9, 3, S.MOVEMENT_TYPE_FACE_DOWN },
  }
  src, mirror, target = ids[1], ids[2], ids[3]

  -- 1.
  local r = { trace() }
  expectEnd(r, 9, 3, target, "1 the beam turns at the mirror and ends on the target")
  expectRow(2, 8, 6, EW, "1 east-west pieces from the source to the mirror, under the player too")
  expect(L.metatile(9, 6) == NW, string.format("1 the north-west corner under the mirror (%03X)", L.metatile(9, 6)))
  expectColumn(9, 4, 5, NS, "1 north-south pieces from the mirror to the target")
  expectFloor(1, 6, "1 the source's own tile is untouched")
  expectFloor(9, 3, "1 the target's tile is untouched")
  expectFloor(10, 6, "1 nothing past the mirror")
  expect(L.block(5, 6) & S.MAPGRID_COLLISION_MASK == 0, "1 a beam tile keeps its collision")
  L.shot("1_to_target")

  -- 2.
  turnMirror("Act3Test_TurnSouthHeader")
  r = { trace() }
  expectEnd(r, 9, 9, 0, "2 turned south, the beam runs to the map's edge")
  expectFloor(9, 5, "2 the old path is floor again")
  expectFloor(9, 4, "2 the old path is floor again")
  expect(L.metatile(9, 6) == SW, string.format("2 the south-west corner under the mirror (%03X)", L.metatile(9, 6)))
  expectColumn(9, 7, 8, NS, "2 north-south pieces south of the mirror")
  expectRow(2, 8, 6, EW, "2 the first leg is drawn again")
  L.shot("2_south")

  -- 3.
  turnMirror("Act3Test_TurnEastHeader")
  r = { trace() }
  expectEnd(r, 9, 6, mirror, "3 the mirror's back ends the beam on the mirror")
  expectFloor(9, 6, "3 no corner under a mirror that doesn't turn the beam")
  expectFloor(9, 7, "3 the south leg is floor again")
  expectFloor(9, 8, "3 the south leg is floor again")

  -- 4.
  turnMirror("Act3Test_TurnWestHeader")
  r = { trace() }
  expectEnd(r, 9, 6, mirror, "4 a mirror facing the beam head-on ends it")

  -- 5.
  turnMirror("Act3Test_TurnNorthHeader")
  r = { trace() }
  expectEnd(r, 9, 3, target, "5 turned north again, the beam reaches the target again")
  expectColumn(9, 4, 5, NS, "5 the north leg is drawn again")
  L.shot("5_to_target_again")
end)
