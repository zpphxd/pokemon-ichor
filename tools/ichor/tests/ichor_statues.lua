-- Marble statues and mirrors, run by tools/ichor/tests/ichor_statues.sh (read it first).
--
-- The Agora's row 6 is the corridor (x 0-12, floor), with (7,7) open below it
-- and a wall at (7,5) above. The player starts at (6,6).
--   A. A statue S at (1,6) facing east, a mirror M at (12,6) facing west (a
--      wall mirror facing the player), a rooted statue R at (9,4).
--      1. Turning on the spot isn't a step: nothing moves.
--      2. A step east, facing M: M shows S behind the player, so S stays. R,
--         unwatched, turns to face the player.
--      3. M turned to face east (its back to the player), a step east: S steps
--         one tile nearer.
--      4. Facing S directly, a step west: S stays.
--      5. Steps south and north, facing neither: S closes in one tile a step,
--         reaches the tile next to the player and touches them: its script
--         runs with VAR_FACING = DIR_NONE and VAR_LAST_TALKED = its local id.
--   B. A rooted statue R at (2,6) facing north and a statue S behind it at (0,6).
--      1. Facing them, a step west: neither moves or turns (statues don't block
--         the line of sight).
--      2. Facing away, a step east: R turns east but stays; S steps nearer.
--   C. A statue S at (1,6), a person P at (3,6) between it and the player.
--      Facing them, a step west: P blocks the view, so S steps nearer.

local L = dofile("tools/ichor/tests/act3_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect = L.expect

local function at(id) return L.objectAt(id) end
local function expectAt(id, x, y, what)
  local ox, oy = at(id)
  expect(ox == x and oy == y, string.format("%s: at (%s,%s), expected (%d,%d)", what, tostring(ox), tostring(oy), x, y))
end
local function expectFacing(id, dir, what)
  local f = L.objectFacing(id)
  expect(f == dir, string.format("%s: faces %s, expected %s", what, L.DIRS[f] or f, L.DIRS[dir]))
end
local function step(key, what)
  local r = L.step(key)
  expect(r == "moved", string.format("%s (the step: %s)", what, r))
  L.waitUntil(L.idle, 300, "the field after " .. what)
end

-- the corridor
local function corridor()
  local open = L.row(0, 12, 6)
  open[#open + 1] = { 7, 7 }
  L.arena(open, { { 7, 5 } })
end

L.start(function()
  L.quickstart()

  -- A. ----------------------------------------------------------------------------------
  L.toSpot(6, 6)
  corridor()
  local touch = L.headers.Act3Test_StatueTouch
  expect(touch ~= nil, "the touch script is in the setup blob")
  local ids = L.place{
    { 1, 6, S.MOVEMENT_TYPE_ICHOR_STATUE_RIGHT, touch },
    { 12, 6, S.MOVEMENT_TYPE_ICHOR_MIRROR_LEFT },
    { 9, 4, S.MOVEMENT_TYPE_ICHOR_STATUE_ROOTED_UP },
  }
  local st, mirror, rooted = ids[1], ids[2], ids[3]
  L.setVar(S.VAR_0x8003, 0)
  L.shot("a_start")

  L.face(K.RIGHT)
  L.wait(10)
  expectAt(st, 1, 6, "A1 turning on the spot moves no statue")
  expectFacing(rooted, S.DIR_NORTH, "A1 the rooted statue hasn't turned")

  step(K.RIGHT, "A2 a step east")
  expectAt(st, 1, 6, "A2 facing the wall mirror, which shows the statue behind: it stays")
  expectFacing(rooted, S.DIR_WEST, "A2 the rooted statue, unwatched, turned to face the player")
  expectAt(rooted, 9, 4, "A2 the rooted statue stays on its plinth")
  L.shot("a2_mirror_watching")

  L.setVar(S.VAR_0x8000, mirror)
  L.runHeader("Act3Test_TurnEastHeader")
  expectFacing(mirror, S.DIR_EAST, "A3 the mirror turned its back to the player")
  step(K.RIGHT, "A3 a step east")
  expectAt(st, 2, 6, "A3 with the mirror's back to the player, the statue stepped one tile nearer")
  expectFacing(st, S.DIR_EAST, "A3 the statue faces the player")
  expectFacing(rooted, S.DIR_SOUTH, "A3 the rooted statue turned again")
  L.shot("a3_statue_moved")

  L.face(K.LEFT)
  L.wait(10)
  expectAt(st, 2, 6, "A4 turning to look isn't a step")
  step(K.LEFT, "A4 a step west, facing the statue")
  expectAt(st, 2, 6, "A4 watched directly, the statue stays")

  step(K.DOWN, "A5 a step south")
  expectAt(st, 3, 6, "A5 facing neither, the statue closes in")
  step(K.UP, "A5 a step north")
  expectAt(st, 4, 6, "A5 again")
  step(K.DOWN, "A5 a step south")
  expectAt(st, 5, 6, "A5 again")
  expect(L.getVar(S.VAR_0x8003) == 0, "A5 no touch yet")
  L.step(K.UP) -- the touch script takes the step's end
  L.waitUntil(L.idle, 300, "the field after the touch script")
  expectAt(st, 6, 6, "A5 the statue reached the tile next to the player")
  expect(L.getVar(S.VAR_0x8003) == 1, string.format("A5 the statue's touch script ran once (%d)", L.getVar(S.VAR_0x8003)))
  expect(L.getVar(S.VAR_0x8006) == S.DIR_NONE, "A5 a touch runs with VAR_FACING = DIR_NONE")
  expect(L.getVar(S.VAR_0x8007) == st, "A5 and VAR_LAST_TALKED = the statue's local id")
  expectFacing(st, S.DIR_EAST, "A5 the statue faces the player it touched")
  L.shot("a5_touch")

  -- B. ----------------------------------------------------------------------------------
  L.toSpot(6, 6)
  corridor()
  ids = L.place{
    { 2, 6, S.MOVEMENT_TYPE_ICHOR_STATUE_ROOTED_UP },
    { 0, 6, S.MOVEMENT_TYPE_ICHOR_STATUE_RIGHT, touch },
  }
  rooted, st = ids[1], ids[2]
  L.face(K.LEFT)
  step(K.LEFT, "B1 a step west, facing both statues")
  expectFacing(rooted, S.DIR_NORTH, "B1 the rooted statue, watched, hasn't turned")
  expectAt(st, 0, 6, "B1 the statue behind it is watched too: statues don't block the view")
  L.face(K.RIGHT)
  step(K.RIGHT, "B2 a step east, facing away")
  expectFacing(rooted, S.DIR_EAST, "B2 the rooted statue turned to face the player")
  expectAt(rooted, 2, 6, "B2 but never moves")
  expectAt(st, 1, 6, "B2 the statue stepped nearer")

  -- C. ----------------------------------------------------------------------------------
  L.toSpot(6, 6)
  corridor()
  ids = L.place{
    { 1, 6, S.MOVEMENT_TYPE_ICHOR_STATUE_RIGHT, touch },
    { 3, 6, S.MOVEMENT_TYPE_FACE_DOWN },
  }
  st = ids[1]
  L.face(K.LEFT)
  step(K.LEFT, "C a step west, facing the statue past a person")
  expectAt(st, 2, 6, "C the person blocks the view, so the statue stepped nearer")
  L.shot("c_person_blocks")
end)
