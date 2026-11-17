-- The bull-leap timing special, run by tools/ichor/tests/ichor_bull_leap.sh (read it first).
--
-- In the Agora, a bull (the map's first object) stands at (1,6) and the player
-- at (11,6), facing it; the line is (10,6), nine tiles from the bull. At
-- F frames a tile the bull starts across the line at frame W = 8 * F of the
-- special (its ninth step), and the window runs W .. W + window - 1. A is
-- pressed when the task's own frame counter reaches a chosen frame:
--   early (frame 20), just early (W - 4), clean (W + 3), just clean
--   (W + window - 4), late (no press), and Mortal's slower bull and wider
--   window, given as the special's defaults (0) are Hero's.
-- VAR_RESULT must be 0 / 1 / 2; an early leap stops the bull on the tile it
-- was crossing, any other ends with it on the line.

local L = dofile("tools/ichor/tests/act3_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local expect, log = L.expect, L.log

local LINE_X, LINE_Y = 10, 6
local bull

-- The special's task, as the address of its data[], or nil.
local function leapTask()
  for i = 0, S.NUM_TASKS - 1 do
    local t = S.gTasks + i * S.TASK_SIZE
    if emu:read8(t + S.OFF_TASK_ACTIVE) ~= 0 and emu:read32(t + S.OFF_TASK_FUNC) == (S.Ichor_BullLeapTask | 1) then
      return t + S.OFF_TASK_DATA
    end
  end
end
local function data(t, i)
  local v = emu:read16(t + 2 * i)
  if v >= 0x8000 then v = v - 0x10000 end
  return v
end
-- task data: 7 frames since the window opened (-1 before), 8 the result (-1
-- while undecided), 9 frames since the special started

-- One leap. pressAt: the task frame to press A on, or nil. window, speed: the
-- special's VAR_0x8006 and VAR_0x8007 (0 for the defaults).
local function leap(pressAt, window, speed, shots)
  bull = L.place{ { 1, 6, S.MOVEMENT_TYPE_FACE_DOWN } }[1]
  L.setVar(S.VAR_0x8004, bull)
  L.setVar(S.VAR_0x8005, LINE_X | (LINE_Y << 8))
  L.setVar(S.VAR_0x8006, window)
  L.setVar(S.VAR_0x8007, speed)
  emu:write16(S.gSpecialVar_Result, 0xFFFF)
  L.runHeader("Act3Test_LeapHeader", { noSettle = true })
  L.waitUntil(function() return leapTask() ~= nil end, 30, "the bull-leap task")
  local pressed, decidedAt, windowAtPress, lastFrame
  local held = 0
  while true do
    local t = leapTask()
    if not t then break end
    lastFrame = data(t, 9)
    if shots and shots[lastFrame] then L.shot(shots[lastFrame]); shots[lastFrame] = nil end
    if pressAt and not pressed and lastFrame >= pressAt then
      emu:addKey(K.A); held = 2; pressed = lastFrame
    elseif held > 0 then
      held = held - 1
      if held == 0 then emu:clearKey(K.A) end
    end
    if not decidedAt and data(t, 8) >= 0 then decidedAt, windowAtPress = data(t, 9), data(t, 7) end
    L.frame()
  end
  emu:clearKey(K.A)
  L.waitUntil(L.idle, 300, "the field after the leap")
  local x, y = L.objectAt(bull)
  return { result = emu:read16(S.gSpecialVar_Result), pressed = pressed, decidedAt = decidedAt,
           windowAtPress = windowAtPress, lastFrame = lastFrame, x = x, y = y }
end

L.start(function()
  L.quickstart()
  L.toSpot(11, 6)
  L.arena(L.row(0, 12, 6))
  L.face(K.LEFT)

  local F, WINDOW = 6, 10
  local W = 8 * F

  local r = leap(20, WINDOW, F)
  log(string.format("NOTE early: A pressed at task frame %d, decided at %s", r.pressed, tostring(r.decidedAt)))
  expect(r.result == S.ICHOR_LEAP_EARLY, string.format("A at frame 20, the bull mid-lane: early (VAR_RESULT %d)", r.result))
  expect(r.decidedAt and r.decidedAt - r.pressed <= 3, "the press counts within 3 frames of the key going down")
  expect(r.x == 5 and r.y == LINE_Y, string.format("an early leap stops the bull on the tile it was crossing: (%d,%d)", r.x, r.y))
  L.shot("early")

  r = leap(W - 4, WINDOW, F)
  expect(r.result == S.ICHOR_LEAP_EARLY, string.format("A at frame %d, 4 frames before the line: early (VAR_RESULT %d)", W - 4, r.result))

  r = leap(W + 3, WINDOW, F, { [1] = "charge_start", [24] = "charge_mid", [W + 1] = "charge_line" })
  expect(r.result == S.ICHOR_LEAP_CLEAN, string.format("A at frame %d, as the bull crosses the line: clean (VAR_RESULT %d)", W + 3, r.result))
  expect(r.windowAtPress and r.windowAtPress > 0, string.format("the window was open at the press (%s frames in)", tostring(r.windowAtPress)))
  expect(r.x == LINE_X and r.y == LINE_Y, string.format("the bull ends on the line: (%d,%d)", r.x, r.y))
  L.shot("clean")

  r = leap(W + WINDOW - 4, WINDOW, F)
  expect(r.result == S.ICHOR_LEAP_CLEAN, string.format("A at frame %d, near the window's end: clean (VAR_RESULT %d)", W + WINDOW - 4, r.result))

  r = leap(nil, WINDOW, F)
  expect(r.result == S.ICHOR_LEAP_LATE, string.format("no A: late (VAR_RESULT %d)", r.result))
  expect(r.lastFrame >= W + WINDOW - 1, string.format("the window stayed open to its end (the task ran to frame %d)", r.lastFrame))
  expect(r.x == LINE_X and r.y == LINE_Y, string.format("the bull ends on the line: (%d,%d)", r.x, r.y))
  L.shot("late")

  -- Mortal: 8 frames a tile, a 14-frame window; then the defaults, Hero's.
  r = leap(8 * 8 + 10, 14, 8)
  expect(r.result == S.ICHOR_LEAP_CLEAN, string.format("Mortal: A at frame %d: clean (VAR_RESULT %d)", 8 * 8 + 10, r.result))
  r = leap(8 * 8 - 6, 14, 8)
  expect(r.result == S.ICHOR_LEAP_EARLY, string.format("Mortal: A at frame %d, when Hero's bull would be on the line: early (VAR_RESULT %d)", 8 * 8 - 6, r.result))
  r = leap(W + 3, 0, 0)
  expect(r.result == S.ICHOR_LEAP_CLEAN, "the defaults (0) are Hero's: 6 frames a tile, a 10-frame window")
end)
